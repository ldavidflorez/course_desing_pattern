# Registro de Cambios

Todos los cambios notables en este proyecto se documentarán en este archivo.

## [Módulo de Validación] - 2025-12-07

### Agregado
- **Módulo de Validación Completo**: Implementado módulo de validación robusto usando patrones Strategy y Chain of Responsibility.
- **ValidationService**: Servicio central que coordina la validación de entidades (productos, categorías, favoritos).
- **Estrategias de Validación**: Implementadas estrategias específicas para cada tipo de entidad con validaciones personalizadas.
- **Manejadores de Validación**: Cadena de responsabilidad con validadores para tipo, rango, existencia y unicidad.
- **Integración DI**: Agregado proveedor de `ValidationService` al contenedor de dependencias.
- **Suite de Pruebas Completa**: Implementadas pruebas unitarias para servicios existentes (HU5) y módulo de validación (HU6) con 96% de cobertura.
- **Documentación Completa**: Creados documentos de diseño, historias de usuario, épica, sprint y presentación del módulo.

### Cambiado
- **Servicios**: Actualizados `ProductService`, `CategoryService` y `FavoriteService` para inyectar y usar `ValidationService` en métodos de creación y actualización.
- **Arquitectura**: Mejorada la arquitectura del proyecto con validaciones consistentes y reutilizables.

### Corregido
- **Importaciones Relativas**: Corregidas rutas de importación en estrategias de validación para compatibilidad con estructura de paquetes.
- **Cadena de Validación**: Corregida configuración de cadena de responsabilidad en estrategias de validación.
- **Validador de Existencia**: Actualizado para manejar validación de productos en favoritos.

## [Mejora DI] - 2025-11-29

### Agregado
- **Contenedor DI Profesional**: Implementada la biblioteca `dependency_injector` para gestión avanzada de inyección de dependencias.
- **AuthContext**: Creada la clase `AuthContext` para encapsular el uso de estrategias de autenticación, siguiendo correctamente el patrón Strategy.
- **Contenedor DI**: Agregado `di_container.py` con proveedores para repositorios, estrategias, servicios y configuración de cableado.

### Cambiado
- **Servicios**: Actualizados todos los servicios (`ProductService`, `CategoryService`, `FavoriteService`) para inyectar `AuthContext` en lugar de `IAuthStrategy` directamente.
- **Blueprints**: Migrados todos los blueprints (`products_bp`, `categories_bp`, `favorites_bp`) para usar el decorador `@inject` con `Provide[Container.*]` para resolución automática de dependencias.
- **Inicialización de App**: Modificado `app.py` para inicializar y cablear el contenedor DI al inicio.

### Removido
- **DI Manual**: Eliminada la instanciación manual de dependencias en blueprints, reemplazada con inyección basada en contenedor.

### Cambiado
- **Diagrama de Arquitectura**: Actualizado `refactored_architecture.puml` para reflejar el uso de AuthContext y la implementación del Contenedor DI.

### Agregado
- **Decorador de Autenticación**: Implementado el decorador `@token_required` en `auth_decorators.py` para validación centralizada de tokens usando DI.

### Removido
- **Autenticación en Servicios**: Eliminados los métodos `authenticate` de todos los servicios (ProductService, CategoryService, FavoriteService) ya que la autenticación ahora se maneja a nivel de blueprint.
- **Verificaciones de Auth Manuales**: Removido código repetitivo de validación de tokens de todas las rutas de blueprints, reemplazado con el decorador `@token_required`.

### Cambiado
- **Diagrama de Arquitectura**: Actualizado `refactored_architecture.puml` para remover métodos `authenticate()` de servicios, remover inyección de AuthContext de servicios y agregar clase AuthDecorator.

## [Refactor] - 2025-11-29

### Agregado
- **Modelos con Patrón Builder**: Creados modelos `Product`, `Category` y `Favorite` con patrón Builder para construcción fluida de objetos.
- **Patrón Repository**: Implementadas interfaces (`IProductRepository`, etc.) e implementaciones basadas en JSON para abstracción de persistencia de datos.
- **Patrón Strategy para Auth**: Agregada interfaz `IAuthStrategy` y `TokenAuthStrategy` para eliminar duplicación de auth.
- **Capa de Servicio**: Introducidos `ProductService`, `CategoryService` y `FavoriteService` para separar lógica de negocio de controladores.
- **Blueprints para Enrutamiento**: Modularizados rutas usando Flask Blueprints (`auth_bp`, `products_bp`, etc.) para mejor organización.
- **Inyección de Dependencias**: Configuración simple de DI en blueprints para repositorios y servicios.

### Cambiado
- **Estructura de App**: Refactorizado `app.py` para registrar blueprints en lugar de recursos Flask-RESTful directos.
- **Endpoints**: Migrados de recursos monolíticos a blueprints basados en servicios, mejorando SRP y testeabilidad.

### Removido
- **Endpoints Antiguos**: Removido directorio `endpoints/` y registro directo de recursos en favor de blueprints y servicios.
- **Directorios Obsoletos**: Removido `utils/` (antigua DatabaseConnection) y `__pycache__/` después de migración completa.

### Agregado
- **Diagramas UML**: Agregados diagramas PlantUML (`diagrams/original_architecture.puml` y `diagrams/refactored_architecture.puml`) para comparar arquitecturas.

## [Refactor] - 2025-11-28

### Corregido
- **Validación de Token**: Corregida discrepancia de token en endpoints de autenticación (productos, categorías, favoritos). Cambiada validación de "abcd1234" a "abcd12345" para coincidir con respuesta de auth.
- **Duplicación en Favoritos**: Corregida duplicación al agregar favoritos reemplazando `add_favorite` con `save_favorites` en método POST.
- **Duplicación en Categorías**: Corregida duplicación al crear/eliminar categorías agregando método `save_categories` y actualizando métodos POST/DELETE.
- **Duplicación en Productos**: Corregida duplicación al crear productos agregando método `save_products` y actualizando método POST.
- **Validación de Categoría**: Agregada validación en creación de productos para asegurar que la categoría existe antes de agregar el producto.
- **Eliminación de Favoritos**: Agregada verificación en DELETE favoritos para retornar 404 si favorito no encontrado, en lugar de siempre 200.
- **Análisis de Categorías**: Removido análisis de argumento duplicado en método DELETE categorías.
- **Verificación de Existencia de Categorías**: Corregida verificación de existencia de categoría en POST categorías para verificar correctamente si el nombre existe.
- **Filtro de Eliminación de Categorías**: Corregido filtro en DELETE categorías para usar nombre de categoría en lugar de objeto.

### Agregado
- **Colección Postman**: Creada `API_Postman_Collection.json` con solicitudes para todos los endpoints (Auth, Productos, Categorías, Favoritos).
- **Métodos de Guardado**: Agregados métodos `save_products`, `save_categories`, `save_favorites` en `DatabaseConnection` para guardado masivo sin duplicación.
- **Validación**: Agregada validación de existencia de categoría en creación de productos.

### Cambiado
- **Conexión de Base de Datos**: Actualizados endpoints para usar métodos `save_*` en lugar de `add_*` para prevenir duplicación.
- **Endpoint de Favoritos**: Cambiado para usar "db.json" en lugar de "favorites.json".

### Removido
- Llamadas `add_*` no utilizadas en endpoints que causaban duplicación.