#!/usr/bin/env python3
"""
Análisis Final PAES 2025 - Establecimientos Excepcionales
Script completo que identifica establecimientos con valor agregado educativo
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
import warnings
warnings.filterwarnings('ignore')

def cargar_y_limpiar_datos(archivo_csv):
    """Carga y limpia los datos con criterios establecidos."""
    df = pd.read_csv(archivo_csv)
    print(f"Datos originales: {len(df)} establecimientos")
    
    # Aplicar filtros de limpieza
    df = df.dropna(subset=['promedioPAES', 'tasaPrioritariosQueRindieronPAES'])
    df = df[
        (df['promedioPAES'] > 0) &
        (df['tasaPrioritariosQueRindieronPAES'] >= 0) & 
        (df['tasaPrioritariosQueRindieronPAES'] <= 1) &
        (df['estudiantesQueRindieronPAES'] >= 5)
    ]
    
    print(f"Datos después de limpieza: {len(df)} establecimientos")
    return df

def analizar_modelo_base(df):
    """Ejecuta análisis de regresión base."""
    X = df['tasaPrioritariosQueRindieronPAES'].values.reshape(-1, 1)
    y = df['promedioPAES'].values
    
    modelo = LinearRegression()
    modelo.fit(X, y)
    
    # Métricas básicas
    r2 = modelo.score(X, y)
    correlacion = np.corrcoef(df['tasaPrioritariosQueRindieronPAES'], df['promedioPAES'])[0, 1]
    
    print(f"\n=== MODELO BASE ===")
    print(f"Ecuación: promedioPAES = {modelo.intercept_:.2f} + {modelo.coef_[0]:.2f} × tasa_prioritarios")
    print(f"R² = {r2:.4f}")
    print(f"Correlación = {correlacion:.4f}")
    
    return modelo, r2

def identificar_establecimientos_excepcionales(df, modelo, top_n=50):
    """Identifica establecimientos con valor agregado excepcional."""
    
    # Calcular predicciones y residuos
    X = df['tasaPrioritariosQueRindieronPAES'].values.reshape(-1, 1)
    y_pred = modelo.predict(X)
    residuos = df['promedioPAES'] - y_pred
    error_std = np.std(residuos)
    
    # Crear DataFrame con métricas
    df_analisis = df.copy()
    df_analisis['puntaje_esperado'] = y_pred
    df_analisis['valor_agregado'] = residuos
    df_analisis['residuo_estandarizado'] = residuos / error_std
    
    # Categorizar contexto de vulnerabilidad
    def categorizar_contexto(tasa):
        if tasa < 0.2:
            return "Baja vulnerabilidad"
        elif tasa < 0.5:
            return "Media vulnerabilidad"
        else:
            return "Alta vulnerabilidad"
    
    df_analisis['contexto_vulnerabilidad'] = df_analisis['tasaPrioritariosQueRindieronPAES'].apply(categorizar_contexto)
    
    # Identificar establecimientos excepcionales (residuo > 2 std)
    excepcionales_positivos = df_analisis[df_analisis['residuo_estandarizado'] > 2].copy()
    excepcionales_negativos = df_analisis[df_analisis['residuo_estandarizado'] < -2].copy()
    
    # Ordenar por valor agregado
    excepcionales_positivos = excepcionales_positivos.nlargest(top_n, 'valor_agregado')
    excepcionales_negativos = excepcionales_negativos.nsmallest(top_n, 'valor_agregado')
    
    return excepcionales_positivos, excepcionales_negativos, df_analisis

def generar_reportes(excepcionales_pos, excepcionales_neg, df_analisis):
    """Genera reportes detallados de establecimientos excepcionales."""
    
    print(f"\n" + "="*80)
    print("ESTABLECIMIENTOS CON VALOR AGREGADO EXCEPCIONAL")
    print("="*80)
    
    # Reporte de establecimientos superiores
    if len(excepcionales_pos) > 0:
        print(f"\n🏆 TOP {len(excepcionales_pos)} ESTABLECIMIENTOS SUPERIORES AL ESPERADO")
        print("-" * 80)
        
        columnas_reporte = ['RBD', 'NOM_RBD', 'NOM_COM_RBD', 'promedioPAES', 'puntaje_esperado', 
                           'valor_agregado', 'tasaPrioritariosQueRindieronPAES', 'contexto_vulnerabilidad']
        
        reporte_pos = excepcionales_pos[columnas_reporte].round(2)
        print(reporte_pos.to_string(index=False))
        
        # Estadísticas por contexto
        print(f"\n📊 DISTRIBUCIÓN POR CONTEXTO DE VULNERABILIDAD:")
        contexto_stats = excepcionales_pos.groupby('contexto_vulnerabilidad').agg({
            'RBD': 'count',
            'valor_agregado': 'mean',
            'promedioPAES': 'mean',
            'tasaPrioritariosQueRindieronPAES': 'mean'
        }).round(2)
        contexto_stats.columns = ['Cantidad', 'Valor_Agregado_Promedio', 'Puntaje_Promedio', 'Tasa_Prioritarios_Promedio']
        print(contexto_stats)
    
    # Reporte de establecimientos inferiores
    if len(excepcionales_neg) > 0:
        print(f"\n⚠️  TOP {len(excepcionales_neg)} ESTABLECIMIENTOS BAJO LO ESPERADO")
        print("-" * 80)
        
        reporte_neg = excepcionales_neg[columnas_reporte].round(2)
        print(reporte_neg.to_string(index=False))

def generar_archivos_salida(excepcionales_pos, excepcionales_neg, df_analisis):
    """Genera archivos CSV con los resultados."""
    
    print(f"\n" + "="*80)
    print("GENERANDO ARCHIVOS DE SALIDA")
    print("="*80)
    
    # Archivo de establecimientos superiores
    if len(excepcionales_pos) > 0:
        archivo_superiores = "establecimientos_valor_agregado_superior_2025.csv"
        columnas_export = ['RBD', 'NOM_RBD', 'COD_DEPE2', 'NOM_COM_RBD', 'promedioPAES', 
                          'estudiantesQueRindieronPAES', 'prioritariosQueRindieronPAES',
                          'tasaPrioritariosQueRindieronPAES', 'puntaje_esperado', 'valor_agregado',
                          'residuo_estandarizado', 'contexto_vulnerabilidad']
        
        excepcionales_pos[columnas_export].to_csv(archivo_superiores, index=False)
        print(f"✅ {archivo_superiores} - {len(excepcionales_pos)} establecimientos")
    
    # Archivo de establecimientos inferiores
    if len(excepcionales_neg) > 0:
        archivo_inferiores = "establecimientos_bajo_esperado_2025.csv"
        excepcionales_neg[columnas_export].to_csv(archivo_inferiores, index=False)
        print(f"✅ {archivo_inferiores} - {len(excepcionales_neg)} establecimientos")
    
    # Archivo completo con análisis
    archivo_completo = "analisis_completo_paes_2025.csv"
    columnas_completo = ['RBD', 'NOM_RBD', 'COD_DEPE2', 'NOM_COM_RBD', 'promedioPAES', 
                        'estudiantesQueRindieronPAES', 'prioritariosQueRindieronPAES',
                        'tasaPrioritariosQueRindieronPAES', 'puntaje_esperado', 'valor_agregado',
                        'residuo_estandarizado', 'contexto_vulnerabilidad']
    
    df_analisis[columnas_completo].to_csv(archivo_completo, index=False)
    print(f"✅ {archivo_completo} - {len(df_analisis)} establecimientos (análisis completo)")

def generar_resumen_ejecutivo(excepcionales_pos, excepcionales_neg, r2):
    """Genera resumen ejecutivo del análisis."""
    
    print(f"\n" + "="*80)
    print("RESUMEN EJECUTIVO")
    print("="*80)
    
    print(f"📈 Modelo explica {r2*100:.1f}% de la variabilidad en puntajes PAES")
    print(f"🏆 {len(excepcionales_pos)} establecimientos con valor agregado excepcional")
    print(f"⚠️  {len(excepcionales_neg)} establecimientos bajo lo esperado")
    
    if len(excepcionales_pos) > 0:
        # Destacar casos de alta vulnerabilidad
        alta_vuln = excepcionales_pos[excepcionales_pos['contexto_vulnerabilidad'] == 'Alta vulnerabilidad']
        if len(alta_vuln) > 0:
            print(f"\n🎯 CASOS DESTACADOS - ALTA VULNERABILIDAD:")
            for _, row in alta_vuln.head(5).iterrows():
                print(f"   • {row['NOM_RBD']} ({row['NOM_COM_RBD']}) - Valor agregado: {row['valor_agregado']:.1f} puntos")
    
    print(f"\n💡 RECOMENDACIONES:")
    print(f"   • Estudiar prácticas pedagógicas de establecimientos con valor agregado")
    print(f"   • Implementar programas de apoyo en establecimientos bajo lo esperado")
    print(f"   • Reconocer públicamente establecimientos excepcionales en contextos vulnerables")

def main():
    """Función principal que ejecuta el análisis completo."""
    
    print("ANÁLISIS FINAL PAES 2025 - ESTABLECIMIENTOS EXCEPCIONALES")
    print("="*80)
    
    # 1. Cargar y limpiar datos
    archivo_csv = "datos_PAES2025_prioritarios.csv"
    df = cargar_y_limpiar_datos(archivo_csv)
    
    # 2. Análisis de modelo base
    modelo, r2 = analizar_modelo_base(df)
    
    # 3. Identificar establecimientos excepcionales
    excepcionales_pos, excepcionales_neg, df_analisis = identificar_establecimientos_excepcionales(df, modelo)
    
    # 4. Generar reportes
    generar_reportes(excepcionales_pos, excepcionales_neg, df_analisis)
    
    # 5. Generar archivos de salida
    generar_archivos_salida(excepcionales_pos, excepcionales_neg, df_analisis)
    
    # 6. Resumen ejecutivo
    generar_resumen_ejecutivo(excepcionales_pos, excepcionales_neg, r2)
    
    print(f"\n" + "="*80)
    print("ANÁLISIS COMPLETADO EXITOSAMENTE")
    print("="*80)

if __name__ == "__main__":
    main()