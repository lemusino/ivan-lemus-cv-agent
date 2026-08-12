Agente de CV — Iván Jesús Lemus Aguilar
Reto IA Banorte · Inteligencia Artificial e Innovación

¿Por qué existe este agente?

Cuando recibí la invitación al reto, supe que iba a ser un desafío real. Quizá no soy el candidato más experto técnicamente, pero le pongo empeño a las cosas — y este agente es prueba de eso.

Este agente no nació de un tutorial. Nació de tres días de intentos, errores, logs y ajustes hasta que la plataforma de Banorte finalmente respondió como debía.

El reto me costó trabajo. Y eso es exactamente lo que quería demostrar.

El problema que nadie documenta:

La instrucción del reto dice: "registra el endpoint público de tu agente compatible con Open Responses". Lo que no dice es exactamente qué campos espera recibir la plataforma ni qué estructura exacta debe tener la respuesta.

Mi primer intento fue un endpoint limpio con el schema básico de Open Responses. La plataforma lo registró sin problema. Pero cuando intenté conversar con el agente desde el chat de hackathon-2024.com, el frontend de React crasheaba con un error críptico sin más contexto.
No sabía si el problema era mi código, el formato de la respuesta, o algo en la plataforma. Así que hice lo que haría en cualquier integración de producción: agregué logging detallado para ver exactamente qué estaba llegando y qué estaba saliendo.

Ahí descubrí dos cosas que nadie documenta:

La plataforma envía campos adicionales en el request que Pydantic rechazaba silenciosamente porque no estaban en mi schema. La solución fue agregar extra = "allow" para ignorar campos desconocidos.
La respuesta necesita incluir "status": "completed" tanto en el objeto raíz como en cada mensaje — sin eso, el frontend no sabe que la respuesta terminó.

Dos líneas de código que me costaron horas encontrar.

¿Por qué elegí este stack?

Gemini (gemini-flash-latest)
Banorte opera sobre Google Cloud Platform. Usar Gemini fue una señal de alineación con su infraestructura real, no solo una decisión técnica. Además, Google AI Studio da acceso gratuito a la API sin tarjeta de crédito.

FastAPI + Python
FastAPI valida el schema de entrada y salida con Pydantic y maneja requests asíncronos sin bloquear el servidor mientras espera la respuesta de Gemini. Para un endpoint que necesita cumplir un contrato de API específico, es la herramienta correcta.

JSON estructurado como knowledge base
Mi primer instinto fue implementar RAG completo con ChromaDB. Lo descarté porque un CV es un documento pequeño y estático — agregar una base de datos vectorial hubiera añadido complejidad sin ningún beneficio real a esta escala. La decisión correcta de arquitectura no siempre es la más sofisticada: es la que resuelve el problema con la menor fricción operativa.

Render + Docker
Empecé con Railway. Pasé más de una hora peleando con su builder automático que fallaba por problemas de red en sus servidores. Migré a Render. Detectó el Dockerfile automáticamente, el deploy tardó menos de dos minutos, y la URL pública funcionó en el primer intento. A veces la decisión correcta es saber cuándo cambiar de herramienta en lugar de seguir peleando con la que no funciona.

GitHub
Control de versiones desde el primer commit. Cada intento fallido quedó documentado en el historial. El repo es público porque el reto lo requiere, pero también porque no tengo nada que esconder en el proceso.



¿Cómo está construido?

Plataforma Banorte (hackathon-2024.com)
         │
         │ POST /v1/responses
         │ Open Responses API format
         ▼
   FastAPI en Render
   (Docker · Python 3.11 · US West)
         │
         ├── Logging de cada request entrante
         ├── Parsing flexible del input
         └── Validación de schema con Pydantic
         │
         ▼
   Gemini Flash (gemini-flash-latest)
   System prompt con CV estructurado en JSON
         │
         ▼
   Respuesta Open Responses
   { id, object, status: "completed", output: [...] }


   Estructura del proyecto:

   ivan-lemus-cv-agent/
├── src/
│   ├── main.py        # Servidor FastAPI, logging, parsing flexible
│   ├── agent.py       # Llamada a Gemini, historial multi-turn
│   └── schemas.py     # Schema Open Responses con extra="allow"
├── data/
│   └── ivan_cv.json   # Knowledge base: CV estructurado
├── Dockerfile
├── requirements.txt
└── README.md

Cómo probarlo:

curl -X POST https://ivan-lemus-cv-agent.onrender.com/v1/responses \
  -H "Content-Type: application/json" \
  -d '{"model":"ivan-cv","input":"¿Cuántos años de experiencia tienes en datos?"}'

  O desde la plataforma del reto: seleccionar el agente "Agente CV Iván Lemus" en hackathon-2024.com/reto-ia/agents.



  Lo que aprendí que no estaba en ningún curso

Construir un agente que funciona localmente es relativamente fácil. Integrarlo con una plataforma externa cuyo contrato de API no está completamente documentado es donde está el trabajo real. El debugging de esa integración — leer los headers, parsear el raw body, comparar lo que llegaba con lo que esperaba — fue la parte más valiosa del ejercicio.

Eso es lo que hace un AI engineer en producción bancaria: no solo construir el modelo, sino hacer que el modelo funcione de forma confiable en un ecosistema de sistemas que no controlas completamente.

Iván Jesús Lemus Aguilar
ivan.jesus.lemus@gmail.com
linkedin.com/in/ivan-jesus-lemus-aguilar
