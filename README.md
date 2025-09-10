# Proyecto1TC

## 📌 Requisitos
- **Python 3.10+**
- Librería `graphviz` instalada en el sistema
- Paquete de Python `graphviz` (`pip install graphviz`)

## Integrantes:
- Adrián Ricardo González Muralles

-  Jose Pablo Ordoñez Barrios

## Comentarios
-Se reemplazaron los '.' por '=' y se eliminó el '*'. Como en el caso de la 3er expresión, así como en sus cadenas: \?(((.|ε)?!?)\*)+ -> \?(((=|ε)?!?))+

-En la 4ta expresión no estamos pidiendo paréntesis literales alrededor de a|x|t; esos paréntesis en la ER son solo de agrupación, no se comparan con '(' y ')' de la cadena. Por lo que los escapamos: if(a|x|t)+\{y\}(else\{n\})? -> if\((a|x|t)+\)\{y\}(else\{n\})?
