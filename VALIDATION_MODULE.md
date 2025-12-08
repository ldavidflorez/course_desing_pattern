# Proyecto de Refactorización de API REST - Grupo

## Punto 1: Integrantes del Grupo + Roles (con Responsabilidades)

Somos dos integrantes en el proyecto:

- **Yhoan**: Líder del Proyecto y Tester. Responsabilidades: Como líder, coordinar el equipo, definir objetivos y plazos, supervisar el progreso general y asegurar la comunicación efectiva entre miembros. Además, liderar reuniones y tomar decisiones finales en disputas. Como tester, diseñar y ejecutar pruebas unitarias, de integración y funcionales, identificar bugs, validar que el código cumpla con los requisitos y documentar resultados de pruebas para asegurar calidad del software.

- **Luis**: Desarrollador Principal y Documentador. Responsabilidades: Implementar el código refactorizado aplicando patrones de diseño, realizar pruebas unitarias y de integración, y documentar el proceso en archivos como REFLECTION.md, CHANGELOG.md y este reporte. También, colaborar en el diseño de la arquitectura y apoyar en testing básico.

## Punto 2: Problemática y Definición del Nuevo Módulo

### Funcionalidades Identificadas que se Beneficiarían de un Nuevo Módulo
A partir del análisis del proyecto refactorizado (rama `refactor`), que implementa una API REST para gestión de productos, categorías y favoritos con autenticación básica, identificamos que las funcionalidades de creación y validación de entidades (productos, categorías y favoritos) se beneficiarían de un nuevo módulo. Actualmente, las validaciones están dispersas en los servicios (e.g., `ProductService.create_product` verifica existencia de categoría) y blueprints, con checks básicos pero insuficientes para tipos de datos, rangos y formatos. Esto genera riesgos de datos inconsistentes y dificulta la extensión.

### Problema Específico que se Va a Resolver o Mejorar
El problema principal es la **falta de validaciones robustas y centralizadas**, identificado como "Insufficient Validation" en REFLECTION.md. Las validaciones actuales son ad-hoc, repetitivas y no cubren aspectos como tipos de datos (e.g., precio debe ser float positivo), rangos (e.g., precio > 0), formatos (e.g., nombre no vacío) o unicidad (e.g., categorías únicas). Esto viola principios SOLID (e.g., SRP en servicios que mezclan lógica de negocio con validación) y puede llevar a errores en `db.json`, debugging difícil y baja mantenibilidad.

### Función y Objetivos del Módulo Dentro del Proyecto
**Función del Módulo**: El módulo de Validación actúa como una capa dedicada a validar entradas de datos antes de procesarlas en los servicios, asegurando que cumplan reglas de negocio y formatos. Centraliza lógica de validación, proporcionando una interfaz uniforme para checks en productos, categorías y favoritos.

**Objetivos**:
- **Centralizar Validaciones**: Extraer y unificar lógica de validación de servicios y blueprints, eliminando duplicación y mejorando SRP.
- **Mejorar Integridad de Datos**: Prevenir entradas inválidas que causen inconsistencias en la base de datos JSON.
- **Facilitar Extensibilidad**: Permitir agregar nuevas validaciones (e.g., para entidades futuras) sin modificar código existente, aplicando OCP.
- **Proporcionar Consistencia**: Generar mensajes de error uniformes y reutilizables en respuestas HTTP.
- **Integración Transparente**: Usar Dependency Injection para inyectar el módulo en servicios, manteniendo la arquitectura limpia.

**Resultado Esperado**: Un sistema más robusto y mantenible, donde validaciones sean confiables, errores sean predecibles y el código sea extensible. Al final, el módulo reducirá bugs relacionados con datos inválidos y facilitará futuras expansiones del proyecto.

## Punto 3: Patrones de Diseño Seleccionados

### Patrones Considerados Más Aplicables
Para el desarrollo del módulo de Validación, seleccionamos los patrones **Strategy** y **Chain of Responsibility**, ambos de tipo comportamiento. Estos patrones son ideales para manejar validaciones dinámicas y secuenciales, permitiendo flexibilidad sin acoplar el código.

- **Strategy Pattern**: Se utiliza para definir familias de algoritmos de validación intercambiables (e.g., `ProductValidationStrategy`, `CategoryValidationStrategy`). Un contexto (`ValidationContext`) selecciona la estrategia basada en el tipo de entidad, delegando la validación específica.
- **Chain of Responsibility Pattern**: Se aplica dentro de cada estrategia para procesar validaciones en secuencia (e.g., primero verificar tipo de dato, luego rango, luego unicidad). Cada "enlace" en la cadena maneja un aspecto y pasa al siguiente si pasa, o retorna errores si falla.

### Justificación de la Elección
La elección se basa en los principios SOLID y las necesidades del proyecto, priorizando mantenibilidad, escalabilidad y claridad del diseño:

- **Mantenibilidad**: Ambos patrones promueven SRP al separar concerns (e.g., validación de tipos vs. rangos en Chain of Responsibility). Strategy facilita cambios en algoritmos sin afectar el contexto, reduciendo bugs y simplificando debugging. En el proyecto actual, esto mejora sobre las validaciones dispersas en servicios, haciendo el código más fácil de actualizar (e.g., añadir una nueva regla de validación solo requiere modificar una estrategia).

- **Escalabilidad**: Strategy permite agregar nuevas estrategias (e.g., para futuras entidades como "usuarios") sin modificar código existente, aplicando OCP. Chain of Responsibility escala bien para validaciones complejas, permitiendo insertar nuevos "handlers" en la cadena dinámicamente. Esto es crucial para un proyecto que podría expandirse (e.g., más endpoints), evitando refactorizaciones masivas.

- **Claridad del Diseño**: Los patrones estructuran el código de manera intuitiva: Strategy abstrae la selección de algoritmos, mientras Chain of Responsibility modela flujos secuenciales naturales. Esto mejora la legibilidad, alineándose con la arquitectura existente (e.g., similar a Strategy en autenticación). Reduce complejidad cognitiva comparado con validaciones monolíticas, facilitando onboarding de nuevos desarrolladores y documentación.

Estos patrones complementan los ya implementados (e.g., Repository, Service Layer), fortaleciendo la cohesión y reduciendo acoplamiento, lo que resulta en un diseño más profesional y alineado con el curso de Patrones de Diseño.

## Punto 4: Diseño de Alto Nivel del Módulo

### Esquema de Alto Nivel
A continuación, presentamos un diagrama de clases UML de alto nivel para el módulo de Validación. El diagrama muestra las clases principales, interfaces, relaciones y patrones aplicados (Strategy y Chain of Responsibility). El módulo se integra con la arquitectura existente mediante Dependency Injection.

Ver el diagrama en `diagrams/validation_module_diagram.puml`.

### Descripción de Clases, Interfaces e Interacciones
- **IValidationStrategy**: Interfaz que define el contrato para estrategias de validación (método `validate`).
- **ValidationContext**: Implementa Strategy Pattern; selecciona y ejecuta la estrategia apropiada basada en el tipo de entidad.
- **ValidationService**: Servicio central que recibe repositorios vía DI y delega validaciones al contexto. Interactúa con `ProductService`, `CategoryService` y `FavoriteService` para validar antes de operaciones.
- **Estrategias Concretas** (ProductValidationStrategy, etc.): Implementan `IValidationStrategy` y usan Chain of Responsibility para validaciones secuenciales.
- **ValidationHandler (Abstract)**: Base para la cadena; cada handler procesa un aspecto (e.g., TypeValidator para tipos de datos) y pasa al siguiente si válido.
- **Interacciones Principales**: El `ValidationService` inyecta repositorios y usa `ValidationContext` para ejecutar estrategias. Dentro de estrategias, la cadena de handlers valida paso a paso. Esto desacopla validaciones, facilitando extensiones (e.g., añadir handlers) sin afectar servicios existentes.

## Punto 5: Plan de Integración con el Proyecto Existente

### ¿Dónde se Conectará el Módulo con el Sistema Actual?
El módulo de Validación se conectará principalmente en la capa de servicios (`services/services.py`), donde se inyectará vía Dependency Injection (`di_container.py`). Específicamente:
- En `ProductService`, `CategoryService` y `FavoriteService`: Antes de operaciones de creación/modificación (e.g., `create_product`), se llamará a `ValidationService.validate_entity()` para validar datos entrantes.
- En los blueprints (`blueprints/*.py`): Los endpoints capturarán errores de validación y retornarán respuestas HTTP consistentes (e.g., 400 Bad Request).
- Con repositorios: El `ValidationService` accederá a `IProductRepository`, `ICategoryRepository` e `IFavoriteRepository` para checks de existencia/unicidad, manteniendo consistencia con la arquitectura existente.

Esto asegura que validaciones ocurran en la capa de negocio, no en presentación, preservando la separación de concerns.

### ¿Qué Partes del Código Actual se Verán Afectadas?
Las partes afectadas serán mínimas y enfocadas en integración, sin cambios disruptivos:
- **Servicios (`services/services.py`)**: Se inyectará `ValidationService` en constructores y se añadirán llamadas a validación en métodos como `create_product`, `create_category` y `add_favorite`. Validaciones existentes (e.g., check de categoría en productos) se moverán al módulo para centralización.
- **Blueprints (`blueprints/products_bp.py`, etc.)**: Se actualizarán para manejar errores de validación (e.g., si `validate_entity` retorna errores, retornar JSON con mensaje). No se cambian rutas o parámetros de endpoints.
- **Contenedor DI (`di_container.py`)**: Se añadirán providers para `ValidationService`, estrategias y handlers, usando patrones Singleton/Factory existentes.
- **Archivos de Configuración**: No se afectan `app.py`, `requirements.txt` o `db.json`. Posiblemente se actualice `REFLECTION.md` y `CHANGELOG.md` para documentar el módulo.

El impacto es bajo, ya que el módulo es aditivo y no requiere reescrituras masivas.

### ¿Cómo Asegurarán Compatibilidad (Interfaces, Endpoints, Adaptadores, etc.)?
Para garantizar compatibilidad, seguiremos principios de diseño y buenas prácticas:
- **Interfaces Consistentes**: El módulo usará interfaces existentes (`IProductRepository`, etc.) y definirá nuevas (`IValidationStrategy`) que sigan contratos claros. Esto evita acoplamiento y facilita mocking en tests.
- **Dependency Injection**: Inyección vía `dependency_injector` asegura que servicios reciban el módulo sin hardcode, manteniendo compatibilidad con la arquitectura actual (e.g., similar a inyección de repositorios).
- **Adaptadores y Wrappers**: Si hay incompatibilidades (e.g., formatos de error), se usarán adaptadores ligeros para mapear respuestas (e.g., convertir dict de errores a JSON HTTP).
- **Endpoints Inalterados**: Los endpoints (`/products`, `/categories`, etc.) no cambiarán; solo se mejorará el manejo de errores (e.g., mensajes más descriptivos). Se mantendrá compatibilidad backward (e.g., respuestas válidas siguen iguales).
- **Testing y Validación**: Se ejecutarán tests existentes para asegurar que integración no rompa funcionalidad. Se añadirán tests unitarios para validadores. Si fallan, se iterará con ajustes mínimos.
- **Versionado y Documentación**: Se documentará en `README.md` y `CHANGELOG.md`. Para producción, se consideraría versionado de API si hay cambios en respuestas.

Esta integración preserva la estabilidad del sistema, aplicando OCP al extender sin modificar código legacy.

## Punto 6: Herramientas Utilizadas y Propósito

Para el desarrollo colaborativo del proyecto y la implementación del módulo de Validación, utilizamos las siguientes herramientas, seleccionadas por su eficacia en coordinación, control de versiones y gestión de tareas:

- **Microsoft Teams**: Utilizado para coordinación y comunicación en tiempo real entre los miembros del equipo (Yhoan y Luis). Facilita reuniones virtuales, chats para discutir ideas, compartir archivos y resolver dudas rápidamente, asegurando una colaboración fluida y reduciendo malentendidos en el diseño e implementación.

- **GitHub**: Empleado para control de versiones del código fuente. Permite gestionar ramas (e.g., `refactor` para el proyecto actual), commits, pull requests y revisiones de código. En este proyecto, se usa para versionar el código refactorizado, incluyendo el nuevo módulo de Validación, y para integrar cambios de manera segura sin conflictos.

- **Jira**: Herramienta para seguimiento y gestión del proyecto. Se utiliza para crear y asignar tareas (e.g., "Implementar ValidationService", "Diseñar diagrama UML"), rastrear progreso, priorizar issues y generar reportes. Ayuda a mantener el proyecto organizado, especialmente en fases como planificación, desarrollo e integración del módulo.

Estas herramientas complementan el flujo de trabajo: Teams para comunicación diaria, GitHub para código y Jira para estructura. No se usan herramientas adicionales como Swagger (ya que la API es simple y documentada en README.md) o Notion (la documentación se maneja en MD y GitHub Wiki), manteniendo el stack minimalista y enfocado en el curso.

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
- **Evidencia de Resultados**: Se entregará un informe de resultados de pruebas (en MD o PDF) con resumen de passed/failed, y el reporte de coverage generado por Pytest (usando `pytest-cov`). Incluye métricas de cobertura (objetivo 80%), capturas de pantalla de reportes y logs de ejecución. No se usará pipeline CI/CD (e.g., GitHub Actions) por simplicidad, pero se ejecutarán tests localmente antes de entrega.