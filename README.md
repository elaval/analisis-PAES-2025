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











