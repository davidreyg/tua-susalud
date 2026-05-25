
﻿
﻿
﻿
﻿
﻿
﻿
﻿
﻿
﻿
﻿
﻿
﻿
﻿
﻿
﻿
## [0.16.0] - 2026-05-25
### 🚀 Nuevas funcionalidades

- :boom: Implementa el servicio y las rutas para la gestión de leyendas en el API ([`0c3ed1b`](https://github.com/davidreyg/tua-susalud/commit/0c3ed1b9e74a101ca4d67c149e64108222cf62d7))

## [0.15.1] - 2026-05-19
### 🐛 Correcciones de errores

- :boom: feat: :sparkles: Elimina la configuración de red externa y ajusta la exposición de puertos en el servicio de base de datos ([`4a4a1c0`](https://github.com/davidreyg/tua-susalud/commit/4a4a1c01f894f6ca6d56a7ad105816efa0e6a2ee))

## [0.15.0] - 2026-05-19
### 🚀 Nuevas funcionalidades

- :sparkles: Optimiza la escritura de datos TUA utilizando asyncio para mejorar el rendimiento ([`92936b4`](https://github.com/davidreyg/tua-susalud/commit/92936b4656d1e088f92f57a2454a3c6b1039eabe))

## [0.14.0] - 2026-05-19
### 🚀 Nuevas funcionalidades

- :sparkles: Agrega encabezado Content-Length en las respuestas de descarga de archivos Excel ([`9150ac9`](https://github.com/davidreyg/tua-susalud/commit/9150ac95ed93cccaf15b1ede070b1482936aaf4b))

## [0.13.0] - 2026-05-19
### 🚀 Nuevas funcionalidades

- :sparkles: Mejora la configuración del Dockerfile, ajustando la copia de archivos y añadiendo la opción de workers en el comando de inicio ([`21ad365`](https://github.com/davidreyg/tua-susalud/commit/21ad365ec550208d97ec02b2b1dde603447d7283))

## [0.12.0] - 2026-05-19
### 🚀 Nuevas funcionalidades

- :sparkles: Agrega configuración de Docker Compose para el servicio de base de datos PostgreSQL y mejora del healthcheck ([`7d3b2b2`](https://github.com/davidreyg/tua-susalud/commit/7d3b2b2a21082fab3c3b41216a097071267270d5))

## [0.11.0] - 2026-05-19
### 🚀 Nuevas funcionalidades

- :sparkles: Agrega endpoint para listar hojas de un archivo Excel y mejora manejo de archivos en ExcelSheetService ([`51febd9`](https://github.com/davidreyg/tua-susalud/commit/51febd9f292249388a6f72930a0eec0b055b7ab5))

## [0.10.0] - 2026-05-19
### 🚀 Nuevas funcionalidades

- :sparkles: Agrega servicio para escribir datos TUA en plantilla Excel y excepciones personalizadas para manejo de errores ([`4af9ce7`](https://github.com/davidreyg/tua-susalud/commit/4af9ce7f7f73685c73c8a13445f89fa423fb582a))

## [0.9.2] - 2026-05-18
### 🐛 Correcciones de errores

- :bug: Omite filas con "SERV. X TERCEROS" en el procesamiento de registros TUA ([`3029c81`](https://github.com/davidreyg/tua-susalud/commit/3029c81c712db3c2673900485441887938ae0f3b))
- :ambulance: Modifica método get_by_sigla para incluir filtro opcional por cargo y actualiza el manejo de turnos en GenerarDataTuaService ([`eed038a`](https://github.com/davidreyg/tua-susalud/commit/eed038a5781079a48ffe1de83f43e28f5b00bfaf))
- :pencil2: Corrige tipado de TuaInputDataRsponse ([`bc59cb1`](https://github.com/davidreyg/tua-susalud/commit/bc59cb1a3036db95e1db1b1c425eef43b3a703ce))

## [0.9.1] - 2026-05-18
### 🐛 Correcciones de errores

- :ambulance: Agrega manejo de turnos en la construcción de registros TUA desde Excel ([`9783102`](https://github.com/davidreyg/tua-susalud/commit/97831024c3f0c77d9d1fda02c1815a7a51c6ad8b))
- :ambulance: Modifica el tipo de datos de 'turnos' en TuaInputDataResponse y agrega método get_by_sigla en LeyendaRepository ([`6595040`](https://github.com/davidreyg/tua-susalud/commit/659504060d70c54e7a4a5cb0653fefabcc68cb7e))

## [0.9.0] - 2026-05-18
### 🚀 Nuevas funcionalidades

- :sparkles: Actualiza configuración de Docker y devcontainer para incluir Python 3.13 y mejorar la conectividad DNS ([`b648dd4`](https://github.com/davidreyg/tua-susalud/commit/b648dd43c4128767c61a64800b8930b2dabd5a11))
### 🐛 Correcciones de errores

- :bug: Actualiza credenciales de base de datos en el archivo de configuración ([`24ef9bc`](https://github.com/davidreyg/tua-susalud/commit/24ef9bc599f794da520db1c37cf34ca8d16706ae))

## [0.8.0] - 2026-05-18
### 🚀 Nuevas funcionalidades

- :sparkles: Agrega archivo Excel TUASUSALUD para generación de datos ([`5602c1e`](https://github.com/davidreyg/tua-susalud/commit/5602c1e03d09f16d5fb6eeda755a64881a75de21))
- :sparkles: Agrega endpoint para generar datos TUA desde archivo Excel ([`0a30dba`](https://github.com/davidreyg/tua-susalud/commit/0a30dba149283cfd02aaea9b4c96fea78b0dff52))
- :sparkles: Agrega repositorio para el modelo Empleado con métodos CRUD ([`352da44`](https://github.com/davidreyg/tua-susalud/commit/352da44b79c8d645fb827c1ab02faa6066ef56f9))
- :sparkles: Agrega modelo y migración para la tabla de empleados ([`6c5512a`](https://github.com/davidreyg/tua-susalud/commit/6c5512a1d9255fd97d47ff0dda040f0e3511a28b))
### 🐛 Correcciones de errores

- :sparkles: Corrige migración y modelo para Empleado ([`16f0884`](https://github.com/davidreyg/tua-susalud/commit/16f088489a4c8ab46f13d968728ba47c2bd15e4b))
- :bricks: Corrige la extracción de datos en el servicio de turno para manejar correctamente los valores numéricos ([`3b0f611`](https://github.com/davidreyg/tua-susalud/commit/3b0f611faf73517aa81bb7987a90578305709b23))

## [0.7.0] - 2026-05-18
### 🚀 Nuevas funcionalidades

- :sparkles: Agrega servicio para lectura de hojas en archivos Excel ([`09c333f`](https://github.com/davidreyg/tua-susalud/commit/09c333fa5719723542404a34f4ec93a5f80acc48))
- :sparkles: Agrega modelos y requests tipados para la API ([`78e708c`](https://github.com/davidreyg/tua-susalud/commit/78e708caadfcb746e15a9515e44ecb15958b17ca))
### 🐛 Correcciones de errores

- :bricks: Corrige rutas ([`9f6b1c5`](https://github.com/davidreyg/tua-susalud/commit/9f6b1c56851b81da4cd5320cc53f831414b39a80))
- :adhesive_bandage: quita prefijo api ([`a683236`](https://github.com/davidreyg/tua-susalud/commit/a68323682dc38bb2323058e89a4912b75d9f6d21))
- :sparkles: Corrige migración y modelo para la tabla leyenda ([`560d0b2`](https://github.com/davidreyg/tua-susalud/commit/560d0b2d72a9b3336b7db8610be2e88c23120dd1))
- :wrench: Expone puerto 5432 de postgresql en devcontainer ([`15397f0`](https://github.com/davidreyg/tua-susalud/commit/15397f01bd16e686e74c255cfbd2324586d747b1))

## [0.6.0] - 2026-05-16
### 🚀 Nuevas funcionalidades

- :sparkles: Agrega funcionalidad para limpiar los Roles de turno en formato excel ([`8d5bf2c`](https://github.com/davidreyg/tua-susalud/commit/8d5bf2c341e6a5af80cf82970a0ab2c8c0f1b8e6))
### 🐛 Correcciones de errores

- 🩹 Agrega pruebas para el servicio de procesamiento de turnos ([`252fe36`](https://github.com/davidreyg/tua-susalud/commit/252fe36e17fd08607cff2c3da63ad26feb77f6db))
- :ambulance: Agrega manejo de excepciones personalizadas y mejora el procesamiento de archivos Excel en el servicio de Turno ([`3b56d58`](https://github.com/davidreyg/tua-susalud/commit/3b56d58f4e3aa486be9bc3ce97b96b0301efdbc4))

## [0.5.0] - 2026-05-16
### 🚀 Nuevas funcionalidades

- :sparkles: Enhance changelog template with commit link macro and update pyproject.toml with repo URL ([`d09518e`](https://github.com/davidreyg/tua-susalud/commit/d09518e6850f219e591070aaec7d728eb57ebf6f))

## [0.4.0] - 2026-05-16
### 🚀 Nuevas funcionalidades

- :sparkles: Update changelog template and enhance change type mapping in pyproject.toml (`bd63ee0`)

## 0.3.0 (2026-05-16)

### Feat

- :sparkles: Add changelog template and change type order to .cz_changelog.md.j2

## 0.2.1 (2026-05-16)

### Fix

- :bug: Update token usage in bumpversion workflow

## 0.2.0 (2026-05-16)

### Feat

- :boom: Cambio de prueba
- :boom: Renombra a TUA SUSALUD
- :tada: Inicio de proyecto

### Fix

- :bug: Remove outdated changelog and update pyrightconfig exclusions
- :bug: Corrige pre commit configuration
- :bug: Corrige pre commit
