#!/usr/bin/env python3
"""
Análisis Final PAES 2025 - Establecimientos con Valor Agregado Excepcional
Script enfocado en reconocer valor agregado educativo
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

def identificar_establecimientos_con_valor_agregado(df, modelo, top_n=50):
    """Identifica SOLO establecimientos con valor agregado excepcional."""
    
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
    
    # Identificar SOLO establecimientos excepcionales POSITIVOS (residuo > 2 std)
    excepcionales_positivos = df_analisis[df_analisis['residuo_estandarizado'] > 2].copy()
    
    # Ordenar por valor agregado
    excepcionales_positivos = excepcionales_positivos.nlargest(top_n, 'valor_agregado')
    
    # Contar establecimientos bajo esperado solo para estadísticas (no para publicar)
    bajo_esperado_count = len(df_analisis[df_analisis['residuo_estandarizado'] < -2])
    
    return excepcionales_positivos, df_analisis, bajo_esperado_count

def generar_reporte_constructivo(excepcionales_pos, df_analisis, bajo_esperado_count):
    """Genera reporte SOLO de establecimientos excepcionales - enfoque constructivo."""
    
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
    
    # Mencionar estadística de bajo esperado SIN detallar establecimientos
    print(f"\n📈 CONTEXTO ESTADÍSTICO:")
    print(f"   • Establecimientos que superan significativamente expectativas: {len(excepcionales_pos)}")
    print(f"   • Establecimientos bajo expectativas estadísticas: {bajo_esperado_count}")
    print(f"   • Nota: No publicamos detalles de establecimientos bajo esperado para evitar estigmatización")

def generar_archivos_constructivos(excepcionales_pos, df_analisis):
    """Genera SOLO archivos constructivos - SIN establecimientos bajo esperado."""
    
    print(f"\n" + "="*80)
    print("GENERANDO ARCHIVOS DE SALIDA - ENFOQUE CONSTRUCTIVO")
    print("="*80)
    
    # Archivo de establecimientos superiores
    if len(excepcionales_pos) > 0:
        archivo_superiores = "establecimientos_valor_agregado_superior_2025.csv"
        columnas_export = ['RBD', 'NOM_RBD', 'COD_DEPE2', 'NOM_COM_RBD', 'promedioPAES', 
                          'estudiantesQueRindieronPAES', 'prioritariosQueRindieronPAES',
                          'tasaPrioritariosQueRindieronPAES', 'puntaje_esperado', 'valor_agregado',
                          'residuo_estandarizado', 'contexto_vulnerabilidad']
        
        excepcionales_pos[columnas_export].to_csv(archivo_superiores, index=False)
        print(f"✅ {archivo_superiores} - {len(excepcionales_pos)} establecimientos con valor agregado excepcional")
    
    # Archivo completo con análisis (para transparencia metodológica)
    archivo_completo = "analisis_completo_paes_2025.csv"
    columnas_completo = ['RBD', 'NOM_RBD', 'COD_DEPE2', 'NOM_COM_RBD', 'promedioPAES', 
                        'estudiantesQueRindieronPAES', 'prioritariosQueRindieronPAES',
                        'tasaPrioritariosQueRindieronPAES', 'puntaje_esperado', 'valor_agregado',
                        'residuo_estandarizado', 'contexto_vulnerabilidad']
    
    df_analisis[columnas_completo].to_csv(archivo_completo, index=False)
    print(f"✅ {archivo_completo} - {len(df_analisis)} establecimientos (análisis completo)")
    
    print(f"\n💡 NOTA IMPORTANTE:")
    print(f"   • Solo publicamos establecimientos con valor agregado excepcional")
    print(f"   • El archivo completo incluye todos los análisis para transparencia metodológica")
    print(f"   • NO generamos listas de establecimientos 'bajo esperado' para evitar estigmatización")

def generar_resumen_ejecutivo_constructivo(excepcionales_pos, r2, bajo_esperado_count):
    """Genera resumen ejecutivo con enfoque constructivo."""
    
    print(f"\n" + "="*80)
    print("RESUMEN EJECUTIVO - ENFOQUE EN VALOR AGREGADO")
    print("="*80)
    
    print(f"📈 Modelo explica {r2*100:.1f}% de la variabilidad en puntajes PAES")
    print(f"🏆 {len(excepcionales_pos)} establecimientos con valor agregado excepcional identificados")
    print(f"📊 {bajo_esperado_count} establecimientos bajo expectativas estadísticas (información solo para contexto)")
    
    if len(excepcionales_pos) > 0:
        # Destacar casos de alta vulnerabilidad
        alta_vuln = excepcionales_pos[excepcionales_pos['contexto_vulnerabilidad'] == 'Alta vulnerabilidad']
        if len(alta_vuln) > 0:
            print(f"\n🎯 CASOS DESTACADOS - ALTA VULNERABILIDAD:")
            for _, row in alta_vuln.head(5).iterrows():
                print(f"   • {row['NOM_RBD']} ({row['NOM_COM_RBD']}) - Valor agregado: {row['valor_agregado']:.1f} puntos")
    
    print(f"\n💡 RECOMENDACIONES CONSTRUCTIVAS:")
    print(f"   • Estudiar y replicar prácticas pedagógicas de establecimientos con alto valor agregado")
    print(f"   • Crear programas de mentoría entre establecimientos excepcionales y otros")
    print(f"   • Desarrollar reconocimientos oficiales basados en valor agregado contextualizado")
    print(f"   • Enfocar recursos en apoyar (no penalizar) establecimientos que requieren mayor apoyo")

def main():
    """Función principal que ejecuta el análisis con enfoque constructivo."""
    
    print("ANÁLISIS PAES 2025 - VALOR AGREGADO EDUCATIVO (ENFOQUE CONSTRUCTIVO)")
    print("="*90)
    
    # 1. Cargar y limpiar datos
    archivo_csv = "datos_PAES2025_prioritarios.csv"
    df = cargar_y_limpiar_datos(archivo_csv)
    
    # 2. Análisis de modelo base
    modelo, r2 = analizar_modelo_base(df)
    
    # 3. Identificar SOLO establecimientos con valor agregado excepcional
    excepcionales_pos, df_analisis, bajo_esperado_count = identificar_establecimientos_con_valor_agregado(df, modelo)
    
    # 4. Generar reporte constructivo
    generar_reporte_constructivo(excepcionales_pos, df_analisis, bajo_esperado_count)
    
    # 5. Generar archivos constructivos
    generar_archivos_constructivos(excepcionales_pos, df_analisis)
    
    # 6. Resumen ejecutivo constructivo
    generar_resumen_ejecutivo_constructivo(excepcionales_pos, r2, bajo_esperado_count)
    
    print(f"\n" + "="*90)
    print("ANÁLISIS COMPLETADO - ENFOQUE CONSTRUCTIVO EXITOSO")
    print("="*90)
    print(f"📁 Archivos generados:")
    print(f"   • establecimientos_valor_agregado_superior_2025.csv")
    print(f"   • analisis_completo_paes_2025.csv")

if __name__ == "__main__":
    main()