# AMZReedemer

Este proyecto es una herramienta automatizada para verificar códigos de gift cards de Amazon. Permite probar múltiples combinaciones y verificar si son válidas utilizando Selenium para la automatización del navegador.

## Características

- 🚀 Automatiza la verificación de códigos de gift cards.
- 🔄 Soporte para múltiples combinaciones de códigos.
- 📈 Usa hilos para aumentar la eficiencia en la verificación.

## Requisitos

- Python 3.x
- Google Chrome instalado
- Las dependencias listadas en `requirements.txt`

## Instalación

Sigue estos pasos para instalar y ejecutar el proyecto:

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/DuckyStripe/AMZReedemer.git
   cd AMZReedemer

2. **Instala las dependencias:** 📦

   Ejecuta el siguiente comando para instalar las dependencias necesarias:

   ```bash
   pip install -r requirements.txt

3. **Configura ChromeDriver:**

   Asegúrate de tener Google Chrome instalado. El script configurará automáticamente ChromeDriver por ti.

## Uso

1. **Inicia el script:**

   Ejecuta el siguiente comando para iniciar el script:

   ```bash
   ️# python AMZReedemer.py

## Sigue las instrucciones:

- Ingresa el patrón del código de la tarjeta cuando se solicite. Usa ? para caracteres desconocidos en el patrón de la tarjeta (por ejemplo, ABCD-123?-EFGH).
## Verifica el resultado:

- El script intentará verificar los códigos ingresados. Los resultados se guardarán en un archivo de texto.
## Notas
Asegúrate de iniciar sesión manualmente en Amazon cuando se abra el navegador.
La sesión y cookies se guardarán para facilitar verificaciones futuras.
## Autor
Este proyecto fue creado por DuckyStripe. Si tienes alguna pregunta o sugerencia, no dudes en contactarme.

## Contribuciones
Las contribuciones son bienvenidas. Por favor, crea un fork del proyecto para realizar cambios y propón un pull request con tus mejoras.

¡Gracias por usar AMZReedemer! 😊