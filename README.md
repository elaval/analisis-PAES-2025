# Análisis de promedios PAES 2025 (rendida en 2024) por establecimeinto

Este repositorio comparte una aproximación alternativa al tradicional "ranking de colegios" que sólo analiza el puntaje absoluto del promedio PAES y considera el contexto socioeconómico del los estudiantes a través del porcentaje de estudiantes prioritarios que rindieron la pueba (AGREGAR REFERENCIA A ESTUDIANTES PRIORITARIOS)

## Fuente de dato

El sitio de Aatos Abiertos del Mineduc publica datos de estudiantes (anonimizados) para usa serie de dimensiones
<img width="626" height="370" alt="image" src="https://github.com/user-attachments/assets/ec6bf7b4-9b51-4547-960f-990a53117793" />

Las tablas con los puntajes de la prueba PAES 2025 (rendida a fines de 2024) tienen los datos de puntaje para cada estudiante identificado con un identificador anónimo denominado MRUN
<img width="969" height="535" alt="image" src="https://github.com/user-attachments/assets/a6744582-d449-4196-87ce-2f67f5f5a6dd" />

También está disponible la tabla con los datos de los estudiantes clasificados como Prioritarios el año 2024, con los estudiantes identificados con el mismo identificador MRUN
<img width="947" height="523" alt="image" src="https://github.com/user-attachments/assets/ecd77024-894d-4420-9096-b71156c7a0e3" />

Con los datos de puntajes PAES es posible obtener el promedio de PAES (comprensión Lectora y Matemática 1) por establecimiento para aquellos estudiantes egresados ese año de cada establecimeinto (RBD identifica al establecimeinto).  En este caso yo realizé consultas SQL (con DuckDB) para agregar los datos.
<img width="640" height="425" alt="image" src="https://github.com/user-attachments/assets/04e6b27b-c056-4c34-a983-9de318c280ad" />

Con la consulta apropiada es posible asociar los datos de puntaje PAES y cantidad de estudiantes que rindieron la prueba que son clasificados como prioritarios por el MINEDUC.

<img width="909" height="509" alt="image" src="https://github.com/user-attachments/assets/fce826ee-6ad6-4d1a-aaf0-687c2d11622b" />

Aquí generé una tabla de datso que contiene:

RBD: identificador del establecimeint
NOM_RBD: comuna
COD_DEPE2: cóigo de dependencia (1 Minicipal, 2 Particular Subvencionado, 3 Particular Pagado, 4 Administración Delegada, 5 Servicio Local)
NOM_COM_RBD: Comuna
promedioPAES: promedio PAES de los estudiantes que rindieron la prueba y reportan puntájes válidos (> 0 en ambas pruebas)
estudiantesQueRindieronPAES: número de estudiantes que rindieron la prueba
prioritariosQueRindieronPAES: cantidad de estudiantes prioritarios que rindieron la prueba
tasaPrioritariosQueRindieronPAES: tasa (entre 0 y 1) de estudiantes prioritarios que rindieron la prueba

Nota:
- Sólo se consideran estabecimientos de educación media de Jóvenes (se excluye educación de adultos)
- Se exlcuyen establecimientos con un número < 5 estudiantes que hayan rendido la prueba (para excluir singularidades como aulas clínicas con 1 estudiante que no es representativa de un establecimiento normal)

# Tabla con datos

La tabla (datos_PAES2025_prioritarios.csv)[datos_PAES2025_prioritarios.csv] contiene los datos de todos los Promedios PAES 2025 (rendida en 2024) y tasa de estudiantes prioritarios que rindieron la prueba para educación media de jóvenes en que hayan rendido 5 o más estudiantes.

# Código de análisis

El Código Python (creado con apoyo de herramientas de Inteligencia Artificia Amazon Q & Claude) executa un análisis de los datos

(analisis_final_paes_2025.py)[analisis_final_paes_2025.py]

Y generó el siguiente reporte:

ANÁLISIS FINAL PAES 2025 - ESTABLECIMIENTOS EXCEPCIONALES
================================================================================
Datos originales: 2942 establecimientos
Datos después de limpieza: 2942 establecimientos

=== MODELO BASE ===
Ecuación: promedioPAES = 718.06 + -240.17 × tasa_prioritarios
R² = 0.6414
Correlación = -0.8008

================================================================================
ESTABLECIMIENTOS CON VALOR AGREGADO EXCEPCIONAL
================================================================================

🏆 TOP 50 ESTABLECIMIENTOS SUPERIORES AL ESPERADO
--------------------------------------------------------------------------------
  RBD                                                  NOM_RBD  NOM_COM_RBD  promedioPAES  puntaje_esperado  valor_agregado  tasaPrioritariosQueRindieronPAES contexto_vulnerabilidad
 3204                                     COLEGIO CONSTITUCION CONSTITUCIÓN        867.73            681.12          186.62                              0.15     Baja vulnerabilidad
12036                                          COLEGIO PINARES  CHIGUAYANTE        883.71            698.05          185.66                              0.08     Baja vulnerabilidad
 9071                                   LICEO AUGUSTO D HALMAR        ÑUÑOA        815.20            649.45          165.76                              0.29    Media vulnerabilidad
 8998                                COLEGIO CAMBRIDGE COLLEGE  PROVIDENCIA        862.03            702.57          159.46                              0.06     Baja vulnerabilidad
 8862                                        COLEGIO TABANCURA     VITACURA        870.83            718.06          152.77                              0.00     Baja vulnerabilidad
 7717                         INSTITUTO ALEMAN DE PUERTO MONTT PUERTO MONTT        861.11            710.32          150.80                              0.03     Baja vulnerabilidad
12085                               COLEGIO CRISTIANO EMMANUEL   LA FLORIDA        698.50            549.95          148.55                              0.70     Alta vulnerabilidad
 8871                            COLEGIO LOS ANDES DE VITACURA     VITACURA        865.65            718.06          147.58                              0.00     Baja vulnerabilidad
 3530                              COLEGIO PARTICULAR SAN JOSE   SAN JAVIER        693.12            547.42          145.70                              0.71     Alta vulnerabilidad
20266                             LICEO BICENTENARIO DE TEMUCO       TEMUCO        760.39            616.18          144.22                              0.42    Media vulnerabilidad
22536                CENTRO EDUCACIONAL SAN SEBASTIAN DE ANCUD        ANCUD        761.71            618.00          143.71                              0.42    Media vulnerabilidad
 8903                    COLEGIO LINCOLN INTERNATIONAL ACADEMY LO BARNECHEA        850.52            708.46          142.06                              0.04     Baja vulnerabilidad
 8868                                     COLEGIO LA GIROUETTE   LAS CONDES        858.59            718.06          140.52                              0.00     Baja vulnerabilidad
24670                              COLEGIO INTERNACIONAL  ALBA        MAIPÚ        848.54            709.17          139.37                              0.04     Baja vulnerabilidad
 8902                         COLEGIO CORDILLERA DE LAS CONDES   LAS CONDES        856.93            718.06          138.86                              0.00     Baja vulnerabilidad
 9271                                  COLEGIO THE KENT SCHOOL  PROVIDENCIA        856.03            718.06          137.96                              0.00     Baja vulnerabilidad
12133                                 COLEGIO FRANCISCO ENCINA        ÑUÑOA        832.40            695.19          137.21                              0.10     Baja vulnerabilidad
 8904                                     COLEGIO SANTA URSULA     VITACURA        854.98            718.06          136.91                              0.00     Baja vulnerabilidad
14498                                         COLEGIO MONTEMAR       CONCÓN        852.47            718.06          134.40                              0.00     Baja vulnerabilidad
 5083                                           COLEGIO ARAUCO       ARAUCO        833.36            700.91          132.45                              0.07     Baja vulnerabilidad
20311                                        COLEGIO HUINGANAL LO BARNECHEA        849.80            718.06          131.74                              0.00     Baja vulnerabilidad
24624                                 COLEGIO TABOR Y NAZARETH LO BARNECHEA        849.55            718.06          131.48                              0.00     Baja vulnerabilidad
25961                                         COLEGIO PALMARES    QUILICURA        795.24            663.77          131.47                              0.23    Media vulnerabilidad
16431                                 COLEGIO  ORCHARD COLLEGE       CURICÓ        848.79            718.06          130.73                              0.00     Baja vulnerabilidad
15576                                        COLEGIO ARRAYANES SAN FERNANDO        848.31            718.06          130.24                              0.00     Baja vulnerabilidad
 9117                 COLEGIO BICENTENARIO MATILDE HUICI NAVAS    PEÑALOLÉN        647.08            517.93          129.16                              0.83     Alta vulnerabilidad
 8873                              COLEGIO VILLA MARIA ACADEMY   LAS CONDES        844.44            718.06          126.38                              0.00     Baja vulnerabilidad
24314                                     COLEGIO CRUZ DEL SUR PUNTA ARENAS        823.46            697.18          126.28                              0.09     Baja vulnerabilidad
 9046                                COLEGIO THE GRANGE SCHOOL     LA REINA        842.98            718.06          124.92                              0.00     Baja vulnerabilidad
 8972                                       COLEGIO SAN BENITO     VITACURA        842.25            718.06          124.19                              0.00     Baja vulnerabilidad
 9051                            COLEGIO ANDREE ENGLISH SCHOOL     LA REINA        839.12            716.17          122.95                              0.01     Baja vulnerabilidad
16604                     INSTITUTO LATINOAMERICANO-EUROPEO DE        TALCA        700.23            577.97          122.26                              0.58     Alta vulnerabilidad
 8000                            INSTITUTO ALEMAN DE FRUTILLAR    FRUTILLAR        747.65            625.69          121.96                              0.38    Media vulnerabilidad
 8996                            COLEGIO SAN IGNACIO EL BOSQUE  PROVIDENCIA        828.73            707.15          121.58                              0.05     Baja vulnerabilidad
 8953                                           COLEGIO HUELEN     VITACURA        839.50            718.06          121.44                              0.00     Baja vulnerabilidad
 5266                                         COLEGIO SAN JOSE        ANGOL        805.28            684.94          120.34                              0.14     Baja vulnerabilidad
 2896         LICEO BICENTENARIO AUGUSTO SANTELICES VALENZUELA     LICANTÉN        655.07            536.61          118.46                              0.76     Alta vulnerabilidad
12025                            COLEGIO ITAHUE DE CHIGUAYANTE  CHIGUAYANTE        814.41            696.23          118.18                              0.09     Baja vulnerabilidad
24762                         COLEGIO SAINT MARY JOSEPH SCHOOL        MACUL        808.02            690.35          117.67                              0.12     Baja vulnerabilidad
24979                                      COLEGIO LOS ALERCES LO BARNECHEA        833.89            718.06          115.83                              0.00     Baja vulnerabilidad
 9237                   INSTITUTO HEBREO DR CHAIM WEIZMANN-ORT LO BARNECHEA        832.12            718.06          114.06                              0.00     Baja vulnerabilidad
 4140 LICEO BICENTENARIO DE EXCELENCIA POLIVALENTE SAN NICOLÁS  SAN NICOLÁS        684.00            570.04          113.95                              0.62     Alta vulnerabilidad
22144                                     COLEGIO PUERTO VARAS PUERTO VARAS        831.93            718.06          113.86                              0.00     Baja vulnerabilidad
26311      COLEGIO LINCOLN INTERN ACADEMY VALLE NORTE CHICUREO       COLINA        831.87            718.06          113.81                              0.00     Baja vulnerabilidad
 8888                                 COLEGIO DEL VERBO DIVINO   LAS CONDES        829.93            716.36          113.56                              0.01     Baja vulnerabilidad
25770                                  LICEO NACIONAL DE MAIPU        MAIPÚ        734.00            621.31          112.69                              0.40    Media vulnerabilidad
 3433                             COLEGIO CONCEPCION DE PARRAL       PARRAL        754.20            642.58          111.62                              0.31    Media vulnerabilidad
16477                                        COLEGIO AQUELARRE         TENO        712.14            601.62          110.52                              0.48    Media vulnerabilidad
15521                                COLEGIO INGLES SAINT JOHN     RANCAGUA        808.74            698.85          109.89                              0.08     Baja vulnerabilidad
16730          LICEO BICENTENARIO ADMINISTRACION Y COMERCIO HC       CURICÓ        684.42            575.11          109.31                              0.60     Alta vulnerabilidad

📊 DISTRIBUCIÓN POR CONTEXTO DE VULNERABILIDAD:
                         Cantidad  ...  Tasa_Prioritarios_Promedio
contexto_vulnerabilidad            ...                            
Alta vulnerabilidad             7  ...                        0.68
Baja vulnerabilidad            35  ...                        0.03
Media vulnerabilidad            8  ...                        0.37

[3 rows x 4 columns]

⚠️  TOP 50 ESTABLECIMIENTOS BAJO LO ESPERADO
--------------------------------------------------------------------------------
  RBD                                                                        NOM_RBD         NOM_COM_RBD  promedioPAES  puntaje_esperado  valor_agregado  tasaPrioritariosQueRindieronPAES contexto_vulnerabilidad
25839                                                         ESC. BAS. Y ESP. CELEI            LO PRADO        465.14            649.45         -184.30                              0.29    Media vulnerabilidad
 9183                                                ESC.PARA SORDOS DR. OTTE GABLER         SAN JOAQUÍN        466.79            649.45         -182.66                              0.29    Media vulnerabilidad
10640                                                               COLEGIO DE MAIPO                BUIN        507.75            688.04         -180.29                              0.12     Baja vulnerabilidad
25373                                                    COLEGIO SAN RAFAEL ARCANGEL            LA REINA        547.50            718.06         -170.56                              0.00     Baja vulnerabilidad
31258                                                    COLEGIO WALDORF DE SANTIAGO               ÑUÑOA        559.29            718.06         -158.78                              0.00     Baja vulnerabilidad
 2250                                      COLEGIO ARTÍSTICO SANTA TERESA DE MACHALI             MACHALÍ        488.15            644.97         -156.82                              0.30    Media vulnerabilidad
 2035                            COLEGIO AGRÍCOLA CUNCUMÉN GONZALO BARROS AMUNÁTEGUI         SAN ANTONIO        501.25            658.02         -156.77                              0.25    Media vulnerabilidad
  129                                                LICEO SUPERIOR GABRIELA MISTRAL             IQUIQUE        502.25            658.02         -155.77                              0.25    Media vulnerabilidad
14428                                                           VINA DEL MAR COLLEGE        VIÑA DEL MAR        570.10            718.06         -147.96                              0.00     Baja vulnerabilidad
40354                                                                     MONTESSORI           LA SERENA        572.94            718.06         -145.13                              0.00     Baja vulnerabilidad
 4561                                                   LICEO JUAN MARTINEZ DE ROZAS          CONCEPCIÓN        507.25            649.45         -142.20                              0.29    Media vulnerabilidad
11766 COLEGIO INSTITUTO ARTÍSTICO DE ESTUDIOS SECUNDARIOS DE LA UNIVERSIDAD DE CHILE            SANTIAGO        579.00            718.06         -139.06                              0.00     Baja vulnerabilidad
 2974                                                    LICEO IGNACIO CARRERA PINTO               TALCA        500.17            638.01         -137.84                              0.33    Media vulnerabilidad
20519                                COLEGIO CIENTIFICO HUMANISTA ALVARO COVARRUBIAS       INDEPENDENCIA        524.92            662.64         -137.72                              0.23    Media vulnerabilidad
 9419                                              LICEO MUNICIPAL ENRIQUE BACKAUSSE PEDRO AGUIRRE CERDA        508.00            638.01         -130.01                              0.33    Media vulnerabilidad
24874                                                   COLEGIO SAN BARTOLOME DE NOS     CALERA DE TANGO        589.33            718.06         -128.73                              0.00     Baja vulnerabilidad
 9228                                                         INSTITUTO PABLO NERUDA               ÑUÑOA        594.78            718.06         -123.29                              0.00     Baja vulnerabilidad
31271                                COLEGIO HIGHLANDS MONTESSORI SCHOOL OF SANTIAGO           PEÑALOLÉN        595.85            718.06         -122.21                              0.00     Baja vulnerabilidad
 9509                                                   COLEGIO SUBERCASEAUX COLLEGE          SAN MIGUEL        573.00            695.19         -122.19                              0.10     Baja vulnerabilidad
 9690                                            CENTRO DUC.CARDENAL JOSE MARIA CARO           LO ESPEJO        467.05            587.06         -120.02                              0.55     Alta vulnerabilidad
26134                                                                 COLEGIO QUIMAY          LAS CONDES        583.16            703.05         -119.90                              0.06     Baja vulnerabilidad
41264                                                               COLEGIO EL ROBLE               ÑUÑOA        558.33            678.04         -119.70                              0.17     Baja vulnerabilidad
 2285                                                COLEGIO MANUEL FRANCISCO CORREA               RENGO        498.54            618.00         -119.45                              0.42    Media vulnerabilidad
24324                                                             GREEN HILL COLLEGE        PUNTA ARENAS        519.67            638.01         -118.34                              0.33    Media vulnerabilidad
 5274                                             LICEO AGRICOLA FORESTAL MANZANARES             RENAICO        450.03            567.96         -117.93                              0.62     Alta vulnerabilidad
24316                                    LICEO POLITEC.CARDENAL RAUL SILVA HENRIQUEZ        PUNTA ARENAS        531.61            649.45         -117.84                              0.29    Media vulnerabilidad
31194                                                             COLEGIO MONTEVERDI           LA SERENA        524.63            642.22         -117.59                              0.32    Media vulnerabilidad
13330                                                     COLEGIO PARTICULAR PIERROT           LA SERENA        521.20            638.01         -116.81                              0.33    Media vulnerabilidad
  284                          LICEO DE HOMBRES DE ANTOFAGASTA MARIO BAHAMONDE SILVA         ANTOFAGASTA        534.03            649.45         -115.41                              0.29    Media vulnerabilidad
25182                                                       LICEO ALCALDE JORGE INDO           QUILICURA        507.27            622.00         -114.73                              0.40    Media vulnerabilidad
 8654                                        COLEGIO POLITECNICO AVDA. INDEPENDENCIA       INDEPENDENCIA        501.59            616.18         -114.58                              0.42    Media vulnerabilidad
 4717                                LICEO TÉCNICO PROFESIONAL LUCILA GODOY ALCAYAGA             HUALPÉN        467.14            580.83         -113.68                              0.57     Alta vulnerabilidad
25197                                           COL.PARTICULAR SAN VALENTIN DE MAIPU               MAIPÚ        567.96            681.12         -113.15                              0.15     Baja vulnerabilidad
24892                                                             SANTA CRUZ COLLEGE         PUENTE ALTO        500.14            612.39         -112.25                              0.44    Media vulnerabilidad
10254                                         CENTRO EDUCACIONAL JOSE MIGUEL CARRERA            RECOLETA        510.20            622.00         -111.80                              0.40    Media vulnerabilidad
12961                                                    LICEO RADOMIRO TOMIC ROMERO              CALAMA        526.46            638.01         -111.55                              0.33    Media vulnerabilidad
 9701                                                   LICEO POLIVALENTE OLOF PALME         LA CISTERNA        507.82            619.17         -111.35                              0.41    Media vulnerabilidad
 9695                                        LICEO POLIVALENTE EUGENIO PEREIRA SALAS PEDRO AGUIRRE CERDA        475.34            582.97         -107.63                              0.56     Alta vulnerabilidad
 8644                                       COLEGIO INDUSTRIAL VASCO NUNEZ DE BALBOA            SANTIAGO        500.40            607.99         -107.59                              0.46    Media vulnerabilidad
24725                                                      COLEGIO JUGENDLAND SCHULE           TALAGANTE        612.29            718.06         -105.78                              0.00     Baja vulnerabilidad
25767                                                COLEGIO SAN JORGE DE LAS CONDES          LAS CONDES        570.78            676.30         -105.51                              0.17     Baja vulnerabilidad
 8501                                   LICEO POLITEC. PDTE. GABRIEL GONZALEZ VIDELA            SANTIAGO        545.32            650.82         -105.50                              0.28    Media vulnerabilidad
 3010                                                  COLEGIO SAN FRANCISCO DE ASIS               TALCA        503.55            608.90         -105.35                              0.45    Media vulnerabilidad
26328                                                       COLEGIO ANTUQUENU ANDINO          LA FLORIDA        613.21            718.06         -104.86                              0.00     Baja vulnerabilidad
12117                                         COMPLEJO EDUCACIONAL J. MIGUEL CARRERA           QUILICURA        492.51            596.60         -104.10                              0.51     Alta vulnerabilidad
14751                                              COLEGIO EL ROBLE DE SANTO DOMINGO       SANTO DOMINGO        546.07            649.45         -103.37                              0.29    Media vulnerabilidad
14324                                                          COLEGIO WILLIAM JAMES        VIÑA DEL MAR        617.36            718.06         -100.71                              0.00     Baja vulnerabilidad
10269                                         LICEO MUNC.ALMIRANTE GALVARINO RIVEROS            CONCHALÍ        527.31            628.00         -100.69                              0.38    Media vulnerabilidad
 9986  LICEO POLITECNICO CAPITAN DE CORBETA INFANTE DE MARINA PEDRO GONZÁLEZ PACHECO       QUINTA NORMAL        520.75            620.85         -100.10                              0.40    Media vulnerabilidad
14418                                                                  COLEGIO PANAL             QUILPUÉ        499.75            597.98          -98.23                              0.50     Alta vulnerabilidad

================================================================================
GENERANDO ARCHIVOS DE SALIDA
================================================================================
✅ establecimientos_valor_agregado_superior_2025.csv - 50 establecimientos
✅ establecimientos_bajo_esperado_2025.csv - 50 establecimientos
✅ analisis_completo_paes_2025.csv - 2942 establecimientos (análisis completo)

================================================================================
RESUMEN EJECUTIVO
================================================================================
📈 Modelo explica 64.1% de la variabilidad en puntajes PAES
🏆 50 establecimientos con valor agregado excepcional
⚠️  50 establecimientos bajo lo esperado

🎯 CASOS DESTACADOS - ALTA VULNERABILIDAD:
   • COLEGIO CRISTIANO EMMANUEL (LA FLORIDA) - Valor agregado: 148.6 puntos
   • COLEGIO PARTICULAR SAN JOSE (SAN JAVIER) - Valor agregado: 145.7 puntos
   • COLEGIO BICENTENARIO MATILDE HUICI NAVAS (PEÑALOLÉN) - Valor agregado: 129.2 puntos
   • INSTITUTO LATINOAMERICANO-EUROPEO DE (TALCA) - Valor agregado: 122.3 puntos
   • LICEO BICENTENARIO AUGUSTO SANTELICES VALENZUELA (LICANTÉN) - Valor agregado: 118.5 puntos

💡 RECOMENDACIONES:
   • Estudiar prácticas pedagógicas de establecimientos con valor agregado
   • Implementar programas de apoyo en establecimientos bajo lo esperado
   • Reconocer públicamente establecimientos excepcionales en contextos vulnerables

## Archivos generados

establecimientos_valor_agregado_superior_2025.csv (50 establecimientos)

establecimientos_bajo_esperado_2025.csv (50 establecimientos)

analisis_completo_paes_2025.csv (2942 establecimientos completos)

# Resumen de resultados
Resumen de Resultados
📊 Modelo Estadístico
R² = 0.6414 (64.1% de variabilidad explicada)

Correlación = -0.8008 (muy fuerte relación negativa)

Ecuación: promedioPAES = 718.06 - 240.17 × tasa_prioritarios

🏆 Establecimientos Excepcionales (50 superiores)
35 de baja vulnerabilidad

8 de media vulnerabilidad

7 de alta vulnerabilidad ⭐ (casos más destacados)

⚠️ Establecimientos Bajo lo Esperado (50)
Incluye escuelas especiales y establecimientos técnicos

Requieren análisis cualitativo adicional

🎯 Casos Más Destacados - Alta Vulnerabilidad
COLEGIO CRISTIANO EMMANUEL (La Florida) - +148.6 puntos

COLEGIO PARTICULAR SAN JOSE (San Javier) - +145.7 puntos

COLEGIO BICENTENARIO MATILDE HUICI NAVAS (Peñalolén) - +129.2 puntos








