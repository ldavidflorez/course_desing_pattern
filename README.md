# Proyecto de Refactorización de API REST

**Universidad Tecnológica de Bolívar**  
**Proyecto de software - fase 1**  
**Curso: Patrones de Diseño de Software**  
**Estudiantes: Luis David Flórez Pareja, Yhoan Smith Mosquera Peñaloza**  
**Diciembre de 2025**

# Descripción

> **Nota importante:** El código original con malas prácticas de codificación está disponible en la rama `main`. Esta rama `refactor` contiene la versión mejorada aplicando patrones de diseño y principios SOLID.

A continuación se presenta una comparación entre una implementación original de una API REST con malas prácticas de codificación y sin diseño de software, y su versión refactorizada. La implementación original (disponible en la rama `main`) sirve como base para aplicar mejoras utilizando patrones de diseño de software, código limpio y principios SOLID.

Esta versión (rama `refactor`) ha sido mejorada aplicando patrones de diseño como Builder, Repository, Strategy, Service Layer, Dependency Injection, Decorator y Blueprints, mejorando la mantenibilidad, testabilidad y extensibilidad.

## Arquitectura

### Arquitectura Original
![Arquitectura Original](out/diagrams/original_architecture/Original%20Architecture.svg)

### Arquitectura Refactorizada
![Arquitectura Refactorizada](out/diagrams/refactored_architecture/Refactored%20Architecture.svg)

Para más detalles sobre los cambios aplicados, incluyendo análisis de code smells, patrones implementados y decisiones de diseño, consulta [REFLECTION.md](REFLECTION.md).

# Cómo Ejecutar

1. **Descarga Python** desde el [Sitio Oficial de Python](https://www.python.org/downloads/).

2. **Instala Python** y configura la variable de entorno.

3. **Abre Git Bash.** Recomiendo usar Git Bash para los siguientes pasos.

4. **Clona este repositorio** o descomprime la carpeta y ve a la carpeta.

5. **Crea un entorno virtual** usando el siguiente comando:
   ```
   python -m venv venv
   ```

6. **Activa el entorno virtual** con este comando:
   ```
   source venv/bin/activate
   ```

7. **Instala las dependencias** ejecutando:
   ```
   pip install -r requirements.txt
   ```

8. **Descarga Postman** desde [Sitio de Postman](https://www.postman.com/downloads/).

9. **Ejecuta** la aplicación Flask con este comando:
   ```
   python app.py
   ```

10. **Usa Postman** para hacer solicitudes a la URL proporcionada por la aplicación Python.

## Cómo Ejecutar con Docker (Alternativa)

Si prefieres usar Docker para ejecutar la aplicación de manera aislada y reproducible, sigue estos pasos:

1. **Instala Docker** desde el [Sitio Oficial de Docker](https://www.docker.com/get-started).

2. **Abre una terminal** en la raíz del proyecto.

3. **Ejecuta el script de build** incluido:
   ```
   sh build.sh
   ```
   Este comando construirá la imagen Docker, detendrá cualquier contenedor anterior, y ejecutará un nuevo contenedor con la aplicación corriendo en `http://localhost:5000`. Los datos de la base de datos se persisten en la carpeta `data/` del host.

4. **Usa Postman** para hacer solicitudes a `http://localhost:5000`.

# Endpoints

1. **Login**: Retorna un token falso para autenticación.
    - **Método**: POST
    - **Ruta**: /auth

2. **Productos**:

   - **Obtener Productos**
     ```
     {
         "method": "GET",
         "path": "/products",
         "authToken": "required"
     }
     ```

   - **Obtener Producto**
     ```
     {
         "method": "GET",
         "path": "/products/productId",
         "authToken": "required"
     }
     ```

   - **Obtener Productos por Categoría**
     ```
     {
         "method": "GET",
         "path": "/products?category=categoryName",
         "authToken": "required"
     }
     ```

   - **Crear Producto**
     ```
     {
         "method": "POST",
         "path": "/products",
         "authToken": "required",
         "body": {
             "name": "nameProduct",
             "category": "categoryProduct",
             "price": 9
         }
     }
     ```

3. **Categorías**

   - **Obtener Categorías**
     ```
     {
         "method": "GET",
         "path": "/categories",
         "authToken": "required"
     }
     ```

   - **Crear Categoría**
     ```
     {
         "method": "POST",
         "path": "/categories",
         "authToken": "required",
         "body": {
             "name": "nameProduct"
         }
     }
     ```

   - **Eliminar Categoría**
     ```
     {
         "method": "DELETE",
         "path": "/categories",
         "authToken": "required",
         "body": {
             "name": "nameProduct"
         }
     }
     ```

4. **Favoritos**

   - **Obtener Favoritos**
     ```
     {
         "method": "GET",
         "path": "/favorites",
         "authToken": "required"
     }
     ```

   - **Agregar Favorito**
     ```
     {
         "method": "POST",
         "path": "/favorites",
         "authToken": "required",
         "body": {
             "user_id": 1,
             "product_id": 1
         }
     }
     ```

   - **Eliminar Favorito**
     ```
     {
         "method": "DELETE",
         "path": "/favorites",
         "authToken": "required",
         "body": {
             "user_id": 1,
             "product_id": 1
         }
     }
     ```

# Documentación Adicional

- **REFLECTION.md**: Documento de reflexión que analiza los code smells identificados en el código original, propone patrones de diseño aplicables y detalla la implementación realizada, incluyendo decisiones de diseño y supuestos.

- **CHANGELOG.md**: Registro de cambios que documenta todas las modificaciones realizadas durante la refactorización, organizadas por fecha y tipo de cambio (agregado, cambiado, corregido, removido).

- **postman/API_Postman_Collection.json**: Colección de Postman con solicitudes preconfiguradas para probar todos los endpoints de la API, facilitando el testing y la validación de la funcionalidad.

- **requirements.txt**: Lista de dependencias Python necesarias para ejecutar la aplicación.

- **data/**: Carpeta que contiene los archivos de base de datos JSON (`db.json` para datos activos y `db_bck.json` como respaldo).

- **diagrams/**: Carpeta con diagramas UML (en formato PlantUML) que ilustran la arquitectura original y refactorizada, ayudando a visualizar los cambios aplicados.

- **Dockerfile** y **build.sh**: Archivos para construir y ejecutar la aplicación en un contenedor Docker, proporcionando una alternativa de despliegue aislada.

Esta refactorización transforma el código de un enfoque procedural a una arquitectura orientada a objetos limpia, aplicando principios SOLID y patrones de diseño para mejorar la calidad del software.

---

# 🛡️ Módulo de Validación: Arquitectura y Diseño

## 📋 Descripción General

El módulo de validación es un componente crítico del sistema refactorizado que implementa una arquitectura robusta y extensible para validar datos de entrada en la API REST. Este módulo aborda uno de los principales problemas identificados en el código original: **falta de validaciones robustas y consistentes**.

### 🎯 Propósito y Alcance

El módulo proporciona:
- **Validación centralizada** de datos para productos, categorías y favoritos
- **Validaciones múltiples** (tipo de datos, rangos, existencia, unicidad)
- **Mensajes de error estructurados** para respuestas HTTP consistentes
- **Extensibilidad** para agregar nuevas reglas de validación
- **Integración perfecta** con la capa de servicios

## 🏗️ Arquitectura del Módulo

### 📁 Estructura de Directorios

```
validators/
├── interfaces.py              # Interfaces abstractas (ISP)
├── validation_context.py      # Contexto del patrón Strategy
├── validation_handler.py      # Handler base para Chain of Responsibility
├── validation_service.py      # Fachada del módulo (Facade Pattern)
├── handlers.py                # Todos los validadores específicos en un archivo
│                              # Contiene: TypeValidator, RangeValidator,
│                              # ExistenceValidator, UniquenessValidator
└── strategies/                # Estrategias de validación por entidad
    ├── category_validator.py
    ├── favorite_validator.py
    └── product_validator.py
```

### 🔄 Flujo de Validación

```
[API Request] → [Blueprint] → [Service Layer] → [Validation Service]
                                                        ↓
[Validation Context] ←→ [Strategy Pattern] ←→ [Chain of Responsibility]
                                                        ↓
[Validation Result] → [Service Response] → [HTTP Response]
```

## 🎨 Patrones de Diseño Implementados

### 1. **Strategy Pattern** - Estrategias de Validación por Entidad

**Implementación:**
```python
class ValidationContext:
    def __init__(self):
        self._strategy: IValidationStrategy = None

    def set_strategy(self, strategy: IValidationStrategy):
        self._strategy = strategy

    def validate(self, data: Dict) -> Dict:
        if self._strategy:
            return self._strategy.validate(data)
        return {'error': 'No validation strategy set'}
```

**Justificación:**
- **Extensibilidad**: Nuevas entidades requieren solo una nueva estrategia
- **Principio Abierto/Cerrado (OCP)**: El contexto no cambia al agregar estrategias
- **Separación de responsabilidades**: Cada estrategia maneja una entidad específica

**Beneficios:**
- ✅ Fácil agregar validaciones para nuevas entidades
- ✅ Código reutilizable entre diferentes contextos
- ✅ Testing independiente por estrategia

### 2. **Chain of Responsibility** - Validaciones Secuenciales

**Implementación:**
```python
class ValidationHandler(ABC):
    def __init__(self):
        self._next_handler: Optional[ValidationHandler] = None

    def set_next(self, handler: 'ValidationHandler') -> 'ValidationHandler':
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, data: Dict) -> Dict:
        pass

    def _handle_next(self, data: Dict) -> Dict:
        if self._next_handler:
            return self._next_handler.handle(data)
        return {}
```

**Uso en Handlers Concretos:**
```python
class TypeValidator(ValidationHandler):
    def handle(self, data: Dict) -> Dict:
        # Lógica de validación específica
        errors = {}
        if 'name' in data and not isinstance(data['name'], str):
            errors['name'] = 'Name must be a string'
        
        # Si hay errores, retornarlos inmediatamente
        if errors:
            return errors
        
        # Pasar al siguiente handler en la cadena
        return self._handle_next(data)
```

**Justificación:**
- **Flexibilidad**: Los handlers pueden reordenarse o reemplazarse dinámicamente
- **Principio de Responsabilidad Única (SRP)**: Cada handler valida un aspecto específico
- **Composición sobre herencia**: Los handlers se componen en tiempo de ejecución

**Beneficios:**
- ✅ Validaciones modulares y reutilizables
- ✅ Fácil agregar/eliminar reglas de validación
- ✅ Orden de validación configurable

### 3. **Interface Segregation Principle (ISP)** - Interfaces Específicas

**Implementación:**
```python
class IValidationStrategy(ABC):
    @abstractmethod
    def validate(self, data: Dict) -> Dict:
        """Valida los datos proporcionados."""
        pass
```

**Justificación:**
- **Interfaces pequeñas y específicas**: Los clientes no dependen de métodos que no usan
- **Acoplamiento reducido**: Cambios en una interfaz no afectan otras
- **Testabilidad mejorada**: Interfaces fáciles de mockear

### 4. **Facade Pattern** - Servicio de Validación Unificado

**Implementación:**
```python
class ProductValidationStrategy(IValidationStrategy):
    def __init__(self, category_repo=None, product_repo=None):
        self.chain = TypeValidator()
        self.chain.set_next(RangeValidator())\
              .set_next(ExistenceValidator(category_repo, 'category'))\
              .set_next(UniquenessValidator(product_repo, 'product'))

    def validate(self, data: Dict) -> Dict:
        return self.chain.handle(data)
```

**Justificación:**
- **Interfaz simplificada**: Los servicios usan una sola llamada para validar cualquier entidad
- **Encapsulación**: Detalles internos del módulo quedan ocultos
- **Mantenibilidad**: Cambios internos no afectan los clientes

## 🔧 Funcionamiento Detallado

### Tipos de Validación Implementados

#### 1. **Validación de Tipos (TypeValidator)**
- Verifica que los campos tengan el tipo de datos correcto (string, int, float)
- Valida campos como name, price, category, user_id, product_id
- Retorna errores específicos por tipo de dato

#### 2. **Validación de Rangos (RangeValidator)**
- Valida rangos numéricos (precios positivos, IDs válidos)
- Verifica que nombres no estén vacíos
- Asegura valores positivos para IDs y precios

#### 3. **Validación de Existencia (ExistenceValidator)**
- Verifica referencias a entidades relacionadas (categorías, productos)
- Consulta repositorios para validar claves foráneas
- Asegura integridad referencial antes de crear relaciones

#### 4. **Validación de Unicidad (UniquenessValidator)**
- Valida que no existan duplicados (ej: nombres de categorías y productos únicos)
- Consulta repositorios para verificar unicidad
- Previene conflictos de datos en entidades que requieren nombres únicos

### Ejemplo de Uso en Servicio

```python
class ProductService:
    def create_product(self, name: str, category: str, price: float):
        # Preparar datos para validación
        data = {"name": name, "category": category, "price": price}

        # Ejecutar validación completa
        errors = self.validation_service.validate_entity("product", data)
        if errors:
            return {"message": "Validation failed", "errors": errors}, 400

        # Proceder con creación si validación pasa
        product = ProductBuilder().set_name(name).set_category(category).set_price(price).build()
        self.product_repo.add(product)
        return {"message": "Product added", "product": product.to_dict()}, 201
```

## 🔗 Integración con el Proyecto

### Relación con Arquitectura General

El módulo de validación se integra perfectamente con la arquitectura refactorizada:

1. **Capa de Presentación (Blueprints)**: Los blueprints capturan requests HTTP
2. **Capa de Servicio**: Los servicios usan el ValidationService antes de procesar datos
3. **Capa de Repositorio**: Los validadores consultan repositorios para verificar existencia
4. **Capa de Modelo**: Los builders crean objetos validados

### Dependencias Inyectadas

```python
# En di_container.py
validation_service = ValidationService(
    category_repo=category_repo,
    product_repo=product_repo
)

# Inyección en servicios
product_service = ProductService(
    product_repo=product_repo,
    category_repo=category_repo,
    validation_service=validation_service
)
```

## 📈 Beneficios y Contribuciones

### 🚀 Eficiencia

- **Validación temprana**: Errores se detectan antes de procesar datos
- **Cadena de validación optimizada**: Se detiene al primer error encontrado
- **Reutilización de validadores**: Los mismos handlers se usan en múltiples estrategias
- **Consultas eficientes**: Los repositorios optimizan las verificaciones de existencia

### 🔧 Escalabilidad

- **Agregar nuevas entidades**: Solo requiere nueva estrategia + configuración
- **Extender validaciones**: Nuevos handlers se integran fácilmente en la cadena
- **Validaciones paralelas**: Múltiples estrategias pueden ejecutarse concurrentemente
- **Configuración externa**: Reglas de validación pueden externalizarse

### 🛠️ Mantenimiento

- **Código modular**: Cada validador tiene responsabilidad única
- **Testing completo**: 96% cobertura en módulo de validación
- **Documentación clara**: Interfaces y contratos bien definidos
- **Principios SOLID**: Código extensible y modificable

### 📊 Métricas de Calidad

- **Cobertura de Tests**: 96% en módulo de validación
- **Complejidad Ciclomática**: Baja (métodos pequeños y enfocados)
- **Acoplamiento**: Reducido mediante inyección de dependencias
- **Cohesión**: Alta (cada clase tiene propósito claro)

## 🧪 Testing y Validación

### Estrategia de Testing

```bash
# Ejecutar tests específicos del módulo
pytest tests/test_validation_*.py -v

# Cobertura del módulo
pytest --cov=validators --cov-report=html
```

### Tests Implementados

- **Unit Tests**: Validadores individuales y estrategias
- **Integration Tests**: Validación end-to-end desde API
- **Edge Cases**: Validaciones con datos inválidos
- **Performance Tests**: Validación de eficiencia en cadenas largas

## 🔮 Extensibilidad Futura

### Agregar Nueva Entidad

1. Crear estrategia específica en `strategies/`
2. Configurar cadena de validación apropiada
3. Registrar en `ValidationService.validate_entity()`
4. Inyectar dependencias necesarias

### Agregar Nuevo Tipo de Validación

1. Crear nuevo handler heredando de `ValidationHandler`
2. Implementar lógica específica en `handle()` (método abstracto)
3. Integrar en estrategias existentes o crear nuevas

### Configuración Externa

- Las reglas de validación pueden externalizarse a archivos YAML/JSON
- Configuración por entorno (desarrollo, producción)
- Validaciones condicionales basadas en contexto

## 📚 Conclusión

El módulo de validación representa una implementación ejemplar de patrones de diseño aplicados a un problema real de software. La combinación de **Strategy**, **Chain of Responsibility**, **ISP** y **Facade** resulta en una solución que es:

- **Robusta**: Validaciones completas y consistentes
- **Mantenible**: Código modular y bien estructurado
- **Extensible**: Fácil agregar nuevas validaciones
- **Testable**: Cobertura completa con tests unitarios e integración (96% cobertura)
- **Performante**: Validación eficiente con detención temprana

Esta implementación demuestra cómo los patrones de diseño, cuando se aplican correctamente, transforman código problemático en soluciones elegantes y profesionales que contribuyen significativamente a la calidad general del software.

---

Esta refactorización transforma el código de un enfoque procedural a una arquitectura orientada a objetos limpia, aplicando principios SOLID y patrones de diseño para mejorar la calidad del software.
