# Elevaris Motors

Static single-page landing site for Elevaris Motors.

## Local verification

From the repository root, run:

```bash
python3 -m unittest discover -s tests -v
awk '/<script>/{f=1;next}/<\/script>/{if(f){f=0}}f' index.html > /tmp/elevaris-inline.js
node --check /tmp/elevaris-inline.js
```

The page references external Google Fonts, Phosphor Icons, GSAP, Pexels video, and Unsplash images at runtime. No build toolchain or server-side application is included in this repository, so production deployment and third-party availability are not verified by the local checks.
