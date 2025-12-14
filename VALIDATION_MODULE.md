# Proyecto de Refactorización de API REST - Grupo

## Punto 1: Integrantes del Grupo + Roles (con Responsabilidades)

Somos dos integrantes en el proyecto:

- **Yhoan**: Líder del Proyecto y Tester. Responsabilidades: Como líder, coordinó el equipo, definió objetivos y plazos, supervisó el progreso general y aseguró la comunicación efectiva entre miembros. Además, lideró reuniones y tomó decisiones finales en disputas. Como tester, diseñó y ejecutó pruebas unitarias, de integración y funcionales, identificó bugs, validó que el código cumpliera con los requisitos y documentó resultados de pruebas para asegurar calidad del software.

- **Luis**: Desarrollador Principal y Documentador. Responsabilidades: Implementó el código refactorizado aplicando patrones de diseño, realizó pruebas unitarias y de integración, y documentó el proceso en archivos como REFLECTION.md, CHANGELOG.md y este reporte. También, colaboró en el diseño de la arquitectura y apoyó en testing básico.

## Punto 2: Problemática y Definición del Nuevo Módulo

### Funcionalidades Identificadas que se Beneficiaron de un Nuevo Módulo
A partir del análisis del proyecto refactorizado (rama `refactor`), que implementó una API REST para gestión de productos, categorías y favoritos con autenticación básica, identificamos que las funcionalidades de creación y validación de entidades (productos, categorías y favoritos) se beneficiaron de un nuevo módulo. Actualmente, las validaciones estaban dispersas en los servicios (e.g., `ProductService.create_product` verificaba existencia de categoría) y blueprints, con checks básicos pero insuficientes para tipos de datos, rangos y formatos. Esto generaba riesgos de datos inconsistentes y dificultaba la extensión.

### Problema Específico que se Va a Resolver o Mejorar
El problema principal fue la **falta de validaciones robustas y centralizadas**, identificado como "Insufficient Validation" en REFLECTION.md. Las validaciones actuales eran ad-hoc, repetitivas y no cubrían aspectos como tipos de datos (e.g., precio debe ser float positivo), rangos (e.g., precio > 0), formatos (e.g., nombre no vacío) o unicidad (e.g., categorías únicas). Esto violaba principios SOLID (e.g., SRP en servicios que mezclaban lógica de negocio con validación) y pudo llevar a errores en `db.json`, debugging difícil y baja mantenibilidad.

### Función y Objetivos del Módulo Dentro del Proyecto
**Función del Módulo**: El módulo de Validación actuó como una capa dedicada a validar entradas de datos antes de procesarlas en los servicios, asegurando que cumplieran reglas de negocio y formatos. Centralizó lógica de validación, proporcionando una interfaz uniforme para checks en productos, categorías y favoritos.

**Objetivos**:
- **Centralizar Validaciones**: Extrajimos y unificamos lógica de validación de servicios y blueprints, eliminando duplicación y mejorando SRP.
- **Mejorar Integridad de Datos**: Previmos entradas inválidas que causaran inconsistencias en la base de datos JSON.
- **Facilitar Extensibilidad**: Permitimos agregar nuevas validaciones (e.g., para entidades futuras) sin modificar código existente, aplicando OCP.
- **Proporcionar Consistencia**: Generamos mensajes de error uniformes y reutilizables en respuestas HTTP.
- **Integración Transparente**: Usamos Dependency Injection para inyectar el módulo en servicios, manteniendo la arquitectura limpia.

**Resultado Esperado**: Un sistema más robusto y mantenible, donde validaciones fueran confiables, errores fueran predecibles y el código fuera extensible. Al final, el módulo redujo bugs relacionados con datos inválidos y facilitó futuras expansiones del proyecto.

## Punto 3: Patrones de Diseño Seleccionados

### Patrones Considerados Más Aplicables
Para el desarrollo del módulo de Validación, seleccionamos los patrones **Strategy** y **Chain of Responsibility**, ambos de tipo comportamiento. Estos patrones fueron ideales para manejar validaciones dinámicas y secuenciales, permitiendo flexibilidad sin acoplar el código.

- **Strategy Pattern**: Se utilizó para definir familias de algoritmos de validación intercambiables (e.g., `ProductValidationStrategy`, `CategoryValidationStrategy`). Un contexto (`ValidationContext`) seleccionó la estrategia basada en el tipo de entidad, delegando la validación específica.
- **Chain of Responsibility Pattern**: Se aplicó dentro de cada estrategia para procesar validaciones en secuencia (e.g., primero verificar tipo de dato, luego rango, luego unicidad). Cada "enlace" en la cadena manejó un aspecto y pasó al siguiente si pasó, o retornó errores si falló.

### Justificación de la Elección
La elección se basó en los principios SOLID y las necesidades del proyecto, priorizando mantenibilidad, escalabilidad y claridad del diseño:

- **Mantenibilidad**: Ambos patrones promovieron SRP al separar concerns (e.g., validación de tipos vs. rangos en Chain of Responsibility). Strategy facilitó cambios en algoritmos sin afectar el contexto, reduciendo bugs y simplificando debugging. En el proyecto actual, esto mejoró sobre las validaciones dispersas en servicios, haciendo el código más fácil de actualizar (e.g., añadir una nueva regla de validación solo requirió modificar una estrategia).

- **Escalabilidad**: Strategy permitió agregar nuevas estrategias (e.g., para futuras entidades como "usuarios") sin modificar código existente, aplicando OCP. Chain of Responsibility escaló bien para validaciones complejas, permitiendo insertar nuevos "handlers" en la cadena dinámicamente. Esto fue crucial para un proyecto que podría expandirse (e.g., más endpoints), evitando refactorizaciones masivas.

- **Claridad del Diseño**: Los patrones estructuraron el código de manera intuitiva: Strategy abstrajo la selección de algoritmos, mientras Chain of Responsibility modeló flujos secuenciales naturales. Esto mejoró la legibilidad, alineándose con la arquitectura existente (e.g., similar a Strategy en autenticación). Redujo complejidad cognitiva comparado con validaciones monolíticas, facilitando onboarding de nuevos desarrolladores y documentación.

Estos patrones complementaron los ya implementados (e.g., Repository, Service Layer), fortaleciendo la cohesión y reduciendo acoplamiento, resultando en un diseño más profesional y alineado con el curso de Patrones de Diseño.

## Punto 4: Diseño de Alto Nivel del Módulo

### Esquema de Alto Nivel
A continuación, presentamos un diagrama de clases UML de alto nivel para el módulo de Validación. El diagrama mostró las clases principales, interfaces, relaciones y patrones aplicados (Strategy y Chain of Responsibility). El módulo se integró con la arquitectura existente mediante Dependency Injection.

![Diagrama de Arquitectura del Módulo de Validación](out/diagrams/validation_module_diagram/Validation%20Module%20High-Level%20Design.svg)

### Descripción de Clases, Interfaces e Interacciones
- **IValidationStrategy**: Interfaz que definió el contrato para estrategias de validación (método `validate`).
- **ValidationContext**: Implementó Strategy Pattern; seleccionó y ejecutó la estrategia apropiada basada en el tipo de entidad.
- **ValidationService**: Servicio central que recibió repositorios vía DI y delegó validaciones al contexto. Interactuó con `ProductService`, `CategoryService` y `FavoriteService` para validar antes de operaciones.
- **Estrategias Concretas** (ProductValidationStrategy, etc.): Implementaron `IValidationStrategy` y usaron Chain of Responsibility para validaciones secuenciales.
- **ValidationHandler (Abstract)**: Base para la cadena; cada handler procesó un aspecto (e.g., TypeValidator para tipos de datos) y pasó al siguiente si válido.
- **Interacciones Principales**: El `ValidationService` inyectó repositorios y usó `ValidationContext` para ejecutar estrategias. Dentro de estrategias, la cadena de handlers validó paso a paso. Esto desacopló validaciones, facilitando extensiones (e.g., añadir handlers) sin afectar servicios existentes.

## Punto 5: Plan de Integración con el Proyecto Existente

### ¿Dónde se Conectará el Módulo con el Sistema Actual?
El módulo de Validación se conectó principalmente en la capa de servicios (`services/services.py`), donde se inyectó vía Dependency Injection (`di_container.py`). Específicamente:
- En `ProductService`, `CategoryService` y `FavoriteService`: Antes de operaciones de creación/modificación (e.g., `create_product`), se llamó a `ValidationService.validate_entity()` para validar datos entrantes.
- En los blueprints (`blueprints/*.py`): Los endpoints capturaron errores de validación y retornaron respuestas HTTP consistentes (e.g., 400 Bad Request).
- Con repositorios: El `ValidationService` accedió a `IProductRepository`, `ICategoryRepository` e `IFavoriteRepository` para checks de existencia/unicidad, manteniendo consistencia con la arquitectura existente.

Esto aseguró que validaciones ocurrieran en la capa de negocio, no en presentación, preservando la separación de concerns.

### ¿Qué Partes del Código Actual se Verán Afectadas?
Las partes afectadas fueron mínimas y enfocadas en integración, sin cambios disruptivos:
- **Servicios (`services/services.py`)**: Se inyectó `ValidationService` en constructores y se añadieron llamadas a validación en métodos como `create_product`, `create_category` y `add_favorite`. Validaciones existentes (e.g., check de categoría en productos) se movieron al módulo para centralización.
- **Blueprints (`blueprints/products_bp.py`, etc.)**: Se actualizaron para manejar errores de validación (e.g., si `validate_entity` retorna errores, retornar JSON con mensaje). No se cambiaron rutas o parámetros de endpoints.
- **Contenedor DI (`di_container.py`)**: Se añadieron providers para `ValidationService`, estrategias y handlers, usando patrones Singleton/Factory existentes.
- **Archivos de Configuración**: No se afectaron `app.py`, `requirements.txt` o `db.json`. Posiblemente se actualizó `REFLECTION.md` y `CHANGELOG.md` para documentar el módulo.

El impacto fue bajo, ya que el módulo fue aditivo y no requirió reescrituras masivas.

### ¿Cómo Asegurarán Compatibilidad (Interfaces, Endpoints, Adaptadores, etc.)?
Para garantizar compatibilidad, seguimos principios de diseño y buenas prácticas:
- **Interfaces Consistentes**: El módulo usó interfaces existentes (`IProductRepository`, etc.) y definió nuevas (`IValidationStrategy`) que siguieron contratos claros. Esto evitó acoplamiento y facilitó mocking en tests.
- **Dependency Injection**: Inyección vía `dependency_injector` aseguró que servicios recibieran el módulo sin hardcode, manteniendo compatibilidad con la arquitectura actual (e.g., similar a inyección de repositorios).
- **Adaptadores y Wrappers**: Si hubo incompatibilidades (e.g., formatos de error), se usaron adaptadores ligeros para mapear respuestas (e.g., convertir dict de errores a JSON HTTP).
- **Endpoints Inalterados**: Los endpoints (`/products`, `/categories`, etc.) no cambiaron; solo se mejoró el manejo de errores (e.g., mensajes más descriptivos). Se mantuvo compatibilidad backward (e.g., respuestas válidas siguen iguales).
- **Testing y Validación**: Se ejecutaron tests existentes para asegurar que integración no rompiera funcionalidad. Se añadieron tests unitarios para validadores. Si fallaron, se iteró con ajustes mínimos.
- **Versionado y Documentación**: Se documentó en `README.md` y `CHANGELOG.md`. Para producción, se consideró versionado de API si hubo cambios en respuestas.

Esta integración preservó la estabilidad del sistema, aplicando OCP al extender sin modificar código legacy.

## Punto 6: Herramientas Utilizadas y Propósito

Para el desarrollo colaborativo del proyecto y la implementación del módulo de Validación, utilizamos las siguientes herramientas, seleccionadas por su eficacia en coordinación, control de versiones y gestión de tareas:

- **Microsoft Teams**: Utilizado para coordinación y comunicación en tiempo real entre los miembros del equipo (Yhoan y Luis). Facilitó reuniones virtuales, chats para discutir ideas, compartir archivos y resolver dudas rápidamente, asegurando una colaboración fluida y reduciendo malentendidos en el diseño e implementación.

- **GitHub**: Empleado para control de versiones del código fuente. Permitió gestionar ramas (e.g., `refactor` para el proyecto actual), commits, pull requests y revisiones de código. En este proyecto, se usó para versionar el código refactorizado, incluyendo el nuevo módulo de Validación, y para integrar cambios de manera segura sin conflictos.

- **Jira**: Herramienta para seguimiento y gestión del proyecto. Se utilizó para crear y asignar tareas (e.g., "Implementar ValidationService", "Diseñar diagrama UML"), rastrear progreso, priorizar issues y generar reportes. Ayudó a mantener el proyecto organizado, especialmente en fases como planificación, desarrollo e integración del módulo.

Estas herramientas complementaron el flujo de trabajo: Teams para comunicación diaria, GitHub para código y Jira para estructura. No se usaron herramientas adicionales como Swagger (ya que la API fue simple y documentada en README.md) o Notion (la documentación se manejó en MD y GitHub Wiki), manteniendo el stack minimalista y enfocado en el curso.

## Punto 7: Estrategia de Desarrollo, Pruebas y Validación

### Metodología Ágil Elegida y Cómo la Aplicarán
Utilizaremos **Scrum-Kanban** como metodología ágil híbrida, combinando la estructura de sprints de Scrum con la flexibilidad de Kanban para flujo continuo. Dado el tiempo limitado (una semana), programaremos un solo sprint de una semana. El sprint incluirá Historias de Usuario (HUs) definidas en Jira, con un backlog priorizado. Usaremos un tablero Kanban en Jira para visualizar el flujo: "To Do" → "In Progress" → "Done". Reuniones diarias cortas en Teams para actualizar progreso, y una retrospectiva al final del sprint. Esto asegura entrega incremental y adaptación rápida.

### Estrategia de Desarrollo
- **Ramas**: Para cada HU (e.g., "Implementar ValidationService"), se creará una rama feature desde `refactor` (e.g., `feature/validation-service`). Al completar, se hará pull request (PR) para merge.
- **Commits**: Commits frecuentes y descriptivos siguiendo conventional commits (e.g., `feat: add IValidationStrategy interface`, `chore: update di_container for validation`, `refactor: extract validation from services`, `fix: handle edge case in RangeValidator`). Esto facilita tracking y automatización.
- **Code Review**: Para cada PR, el otro integrante revisará código en GitHub, verificando patrones, tests y documentación. Se requiere aprobación antes de merge para asegurar calidad.

### Estrategia de Pruebas
Dado que el desarrollo actual no cuenta con pruebas unitarias, un primer paso será crear una suite básica de tests para el código existente (e.g., servicios, repositorios) antes de integrar el módulo nuevo. Esto establecerá una base sólida y permitirá validar que el módulo no rompa funcionalidad legacy.

- **Pruebas Unitarias**: Cubrirán al menos 80% del código, enfocándose en clases del módulo (e.g., `ValidationService`, estrategias, handlers). Usaremos Pytest para validar lógica individual: e.g., `TypeValidator` maneja tipos correctos, `RangeValidator` rechaza valores fuera de rango. También tests para interfaces y excepciones. Para el código existente, se añadirán tests básicos (e.g., `ProductService.get_all_products` retorna lista correcta).
- **Pruebas de Integración**: Validarán escenarios end-to-end: e.g., integración con servicios (`ProductService` llama a validación antes de crear producto), DI container inyecta dependencias correctamente, y endpoints retornan errores apropiados. Escenarios incluyen creación válida/inválida de productos/categorías, y compatibilidad con repositorios JSON.
- **Evidencia de Resultados**: Se entregó un informe de resultados de pruebas (en MD o PDF) con resumen de passed/failed, y el reporte de coverage generado por Pytest (usando `pytest-cov`). Incluyó métricas de cobertura (objetivo 80%), capturas de pantalla de reportes y logs de ejecución. No se usó pipeline CI/CD (e.g., GitHub Actions) por simplicidad, pero se ejecutaron tests localmente antes de entrega.