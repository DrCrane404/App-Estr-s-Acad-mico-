class CuestionarioSemanal:
    def __init__(self):
        self.preguntas = self._definir_preguntas()
    
    def _definir_preguntas(self):
        return [
            {
                "id": 1,
                "texto": "¿Con qué frecuencia te has sentido abrumado/a por tus tareas académicas esta semana?",
                "opciones": [
                    {"texto": "Nunca", "peso": 0},
                    {"texto": "Casi nunca", "peso": 1},
                    {"texto": "A veces", "peso": 2},
                    {"texto": "A menudo", "peso": 3},
                    {"texto": "Siempre", "peso": 4}
                ]
            },
            {
                "id": 2,
                "texto": "¿Cómo ha sido la calidad de tu sueño esta semana?",
                "opciones": [
                    {"texto": "Muy mala", "peso": 4},
                    {"texto": "Mala", "peso": 3},
                    {"texto": "Regular", "peso": 2},
                    {"texto": "Buena", "peso": 1},
                    {"texto": "Muy buena", "peso": 0}
                ]
            },
            {
                "id": 3,
                "texto": "¿Has podido cumplir con tus horarios y entregas planificadas?",
                "opciones": [
                    {"texto": "Siempre", "peso": 0},
                    {"texto": "Casi siempre", "peso": 1},
                    {"texto": "A veces", "peso": 2},
                    {"texto": "Casi nunca", "peso": 3},
                    {"texto": "Nunca", "peso": 4}
                ]
            },
            {
                "id": 4,
                "texto": "¿Has sentido síntomas físicos de estrés (dolor de cabeza, tensión muscular, fatiga)?",
                "opciones": [
                    {"texto": "Mucho", "peso": 4},
                    {"texto": "Bastante", "peso": 3},
                    {"texto": "Algo", "peso": 2},
                    {"texto": "Poco", "peso": 1},
                    {"texto": "Nada", "peso": 0}
                ]
            },
            {
                "id": 5,
                "texto": "En general, ¿cómo calificarías tu nivel de estrés esta semana?",
                "opciones": [
                    {"texto": "Muy bajo", "peso": 0},
                    {"texto": "Bajo", "peso": 1},
                    {"texto": "Moderado", "peso": 2},
                    {"texto": "Alto", "peso": 3},
                    {"texto": "Muy alto", "peso": 4}
                ]
            }
        ]
    
    def calcular_nivel_estres(self, respuestas_usuario):
        """
        respuestas_usuario: dict con ids de pregunta como clave y el índice de la opción seleccionada como valor.
        Ejemplo: {1: 2, 2: 4, 3: 1, 4: 0, 5: 3}
        """
        puntaje_obtenido = 0
        puntaje_maximo = 0
        for pregunta in self.preguntas:
            id_preg = pregunta["id"]
            opciones = pregunta["opciones"]
            max_peso = max(op["peso"] for op in opciones)
            puntaje_maximo += max_peso
            idx = respuestas_usuario.get(id_preg, 0)
            if 0 <= idx < len(opciones):
                puntaje_obtenido += opciones[idx]["peso"]
            else:
                puntaje_obtenido += max_peso  # fallback
        nivel = (puntaje_obtenido / puntaje_maximo) * 10 if puntaje_maximo > 0 else 0
        return round(nivel, 1)