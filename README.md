# Análisis de Valor Agregado Educativo - PAES 2025

## 🎯 Propósito del Análisis

Este repositorio presenta una **aproximación alternativa** al tradicional "ranking de colegios" que considera únicamente puntajes absolutos. Nuestro enfoque evalúa el **valor agregado educativo** que cada establecimiento genera considerando su contexto socioeconómico.

### ¿Por qué es importante?

Los rankings tradicionales pueden perpetuar desigualdades al no considerar que establecimientos en contextos socioeconómicos más desafiantes requieren mayor esfuerzo para alcanzar buenos resultados. Este análisis identifica establecimientos que **superan significativamente** las expectativas estadísticas basadas en su contexto de vulnerabilidad.

## 📊 Metodología

### Datos Utilizados

Utilizamos datos oficiales del MINEDUC disponibles en el [sitio de Datos Abiertos](https://datosabiertos.mineduc.cl/):

1. **Puntajes PAES 2025** (rendida en 2024): Comprensión Lectora y Matemática 1
2. **Estudiantes Prioritarios 2024**: Clasificación oficial de vulnerabilidad socioeconómica
3. **Datos de Establecimientos**: RBD, nombres, comunas y dependencia administrativa

### Modelo Estadístico

Aplicamos **regresión lineal** para predecir puntajes esperados:

```
Puntaje PAES Esperado = 718.06 - 240.17 × Tasa de Estudiantes Prioritarios
```

**Interpretación**: Por cada 10% adicional de estudiantes prioritarios, el puntaje promedio disminuye en 24 puntos.

- **R² = 0.641**: El modelo explica 64.1% de la varianza en puntajes
- **Correlación = -0.80**: Relación fuerte entre vulnerabilidad y rendimiento

### Criterios de Clasificación

**Establecimientos con Valor Agregado Excepcional**:
- Puntaje real > 2 desviaciones estándar por sobre el esperado
- Mínimo 5 estudiantes que rindieron PAES
- Solo educación media de jóvenes (excluye educación adultos)

## 📈 Resultados Principales

### Estadísticas Generales

| Métrica | Valor |
|---------|-------|
| **Establecimientos analizados** | 2,942 |
| **Varianza explicada por contexto socioeconómico** | 64.1% |
| **Establecimientos con valor agregado excepcional** | 50 |
| **Correlación vulnerabilidad-puntaje** | -0.80 |

### Distribución por Contexto de Vulnerabilidad

| Contexto | Establecimientos Excepcionales | Porcentaje |
|----------|-------------------------------|------------|
| **Baja vulnerabilidad** (< 20% prioritarios) | 35 | 70% |
| **Media vulnerabilidad** (20-50% prioritarios) | 8 | 16% |
| **Alta vulnerabilidad** (> 50% prioritarios) | 7 | 14% |

### Casos Destacados - Alta Vulnerabilidad 🏆

| Establecimiento | Comuna | Valor Agregado | % Prioritarios | Puntaje PAES |
|----------------|--------|---------------|----------------|--------------|
| **Colegio Cristiano Emmanuel** | La Florida | +149 puntos | 70% | 699 |
| **Colegio Particular San José** | San Javier | +146 puntos | 71% | 693 |
| **Liceo Bicentenario Matilde Huici Navas** | Peñalolén | +129 puntos | 83% | 647 |
| **Instituto Latinoamericano-Europeo** | Talca | +122 puntos | 58% | 700 |
| **Liceo Bicentenario Augusto Santelices** | Licantén | +118 puntos | 76% | 655 |

> **Nota**: Estos establecimientos demuestran que la excelencia educativa es posible incluso en contextos de alta vulnerabilidad socioeconómica.

## 📁 Archivos del Repositorio

### Datos de Entrada
- **`datos_PAES2025_prioritarios.csv`**: Dataset consolidado con puntajes PAES y contexto socioeconómico

### Scripts de Análisis
- **`analisis_final_paes_2025.py`**: Script principal con modelo estadístico y generación de resultados

### Resultados
- **`analisis_completo_paes_2025.csv`**: Análisis completo de los 2,942 establecimientos
- **`establecimientos_valor_agregado_superior_2025.csv`**: Top 50 establecimientos con valor agregado excepcional

### Visualizaciones
- **`analisis_regresion_paes_2025.png`**: Gráficos del modelo estadístico y validación

## 🔍 Estructura de los Datos

### Dataset Principal (`datos_PAES2025_prioritarios.csv`)

| Campo | Descripción |
|-------|-------------|
| `RBD` | Identificador único del establecimiento |
| `NOM_RBD` | Nombre del establecimiento |
| `COD_DEPE2` | Código de dependencia (1=Municipal, 2=Part.Subv., 3=Part.Pagado, 4=Adm.Delegada, 5=Servicio Local) |
| `NOM_COM_RBD` | Comuna del establecimiento |
| `promedioPAES` | Promedio PAES (Comprensión Lectora + Matemática 1) |
| `estudiantesQueRindieronPAES` | Número de estudiantes que rindieron |
| `prioritariosQueRindieronPAES` | Estudiantes prioritarios que rindieron |
| `tasaPrioritariosQueRindieronPAES` | Tasa de estudiantes prioritarios (0-1) |

### Dataset de Resultados (`establecimientos_valor_agregado_superior_2025.csv`)

Campos adicionales en resultados:
- `puntaje_esperado`: Puntaje predicho por el modelo estadístico
- `valor_agregado`: Diferencia entre puntaje real y esperado
- `residuo_estandarizado`: Residuo en unidades de desviación estándar
- `contexto_vulnerabilidad`: Clasificación de vulnerabilidad (Baja/Media/Alta)

## 🎓 Definiciones Clave

**Estudiantes Prioritarios**: Clasificación oficial del MINEDUC para estudiantes en condición de vulnerabilidad socioeconómica, basada en criterios del Registro Social de Hogares.

**Valor Agregado**: Diferencia entre el puntaje real obtenido por un establecimiento y el puntaje esperado según su contexto socioeconómico.

**Residuo Estandarizado**: Medida que indica cuántas desviaciones estándar está un establecimiento por sobre o bajo lo esperado.

## 💡 Implicaciones y Usos

### Para Familias
- Evaluar opciones educacionales considerando el contexto, no solo puntajes absolutos
- Identificar establecimientos que agregan valor real en el proceso educativo

### Para Autoridades Educacionales
- Reconocer y estudiar prácticas exitosas en contextos desafiantes
- Orientar recursos y apoyo hacia establecimientos que más lo necesiten
- Desarrollar indicadores más equitativos de calidad educativa

### Para Investigadores
- Base de datos para estudios sobre eficacia escolar
- Metodología replicable para análisis de valor agregado

## ⚖️ Consideraciones Éticas

- **No publicamos listas de establecimientos "bajo lo esperado"** para evitar estigmatización
- **Enfoque constructivo**: Buscamos reconocer buenas prácticas, no clasificar negativamente
- **Transparencia metodológica**: Todo el código y datos están disponibles para revisión

## 🔗 Enlaces Relevantes

- [Datos Abiertos MINEDUC](https://datosabiertos.mineduc.cl/)
- [Información sobre Estudiantes Prioritarios](https://www.ayudamineduc.cl/ficha/estudiantes-prioritarios-4)

## 📝 Cómo Citar Este Trabajo

```
Laval, E. (2025). Análisis de Valor Agregado Educativo - PAES 2025. 
Repositorio GitHub: https://github.com/elaval/analisis-PAES-2025
```

## 🤝 Contribuciones

¿Ideas para mejorar el análisis? ¿Encontraste algún error? Las contribuciones son bienvenidas:

1. Abre un **Issue** para discutir cambios
2. Envía un **Pull Request** con mejoras
3. Comparte feedback en [@elaval](https://twitter.com/elaval)

## 📄 Licencia

Este proyecto se comparte bajo licencia MIT. Los datos utilizados son de dominio público del MINEDUC.

---

*"La verdadera excelencia educativa se mide no solo por dónde llegan los estudiantes, sino por cuánto avanzan desde donde partieron."*