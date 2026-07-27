# Publicación del programa MRC-2026

Esta carpeta es el sitio listo para subir. No requiere servidor de
aplicación, base de datos ni proceso de compilación: son archivos estáticos.

## Qué subir

Todo el contenido de esta carpeta a la raíz del sitio o a un subdirectorio,
respetando la estructura:

    index.html
    certificado.html
    modulos/m01.html … m08.html
    .nojekyll
    AuditCaats_MRC2026.html   (opcional: copia del programa en un solo archivo)

La carpeta `backend/` NO se sube al sitio web: su contenido va al proyecto de
Google Apps Script.

## Opciones de alojamiento

Cualquiera sirve. En orden de simplicidad:

- Netlify o Cloudflare Pages: arrastrar la carpeta sobre el panel.
- GitHub Pages: subir al repositorio y activar Pages. El archivo `.nojekyll`
  ya viene incluido.
- Hosting propio: copiar por FTP al directorio público.

## Después de publicar

1. Abrir el sitio y comprobar que el logo aparece en la cabecera.
2. Inscribirse con datos de prueba y completar un módulo entero.
3. Verificar que el certificado imprime bien en A4 vertical.
4. Confirmar que el código del certificado se registra en la planilla del
   backend.

## Backend de certificación

En el proyecto de Apps Script existente: reemplazar `1_Codigo.gs`, agregar
`verificar.html` y publicar con **Administrar implementaciones → Editar →
Versión nueva**. Crear una implementación nueva cambia la URL y deja sin
verificación los certificados ya emitidos.

La URL `/exec` debe quedar cargada en `assets/ac_programa.js` **antes** de
ejecutar `empaquetar.py`.
