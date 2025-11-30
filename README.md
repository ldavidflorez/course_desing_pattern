# Proyecto de Refactorización de API REST

**Universidad Tecnológica de Bolívar**  
**Hacia un código más legible y mantenible en el tiempo**  
**Curso: Patrones de Diseño de Software**  
**Estudiante: Luis David Flórez Pareja**  
**Noviembre de 2025**

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
