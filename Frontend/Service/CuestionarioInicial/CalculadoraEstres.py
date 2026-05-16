class CalculadoraEstres:
    
    def __init__(self):
        self.cuestionario = {
            "total_preguntas": 23,
            "preguntas": self._definir_preguntas()
        }
    
    def _definir_preguntas(self):
        preguntas = []
        
        preguntas.append({
            "id": 1,
            "texto": "¿Cuántas horas duermes al día? En promedio",
            "categoria": "sueño",
            "opciones": [
                {"texto": "De 3-5 horas", "peso": 4},
                {"texto": "De 5-7 horas", "peso": 2},
                {"texto": "De 7-9 horas", "peso": 0}
            ]
        })
        
        preguntas.append({
            "id": 2,
            "texto": "¿Cómo calificarías la calidad general de tu sueño?",
            "categoria": "sueño",
            "opciones": [
                {"texto": "Muy mala", "peso": 4},
                {"texto": "1", "peso": 3},
                {"texto": "2", "peso": 2},
                {"texto": "3", "peso": 2},
                {"texto": "4", "peso": 1},
                {"texto": "5 (Muy buena)", "peso": 0}
            ]
        })
        
        preguntas.append({
            "id": 3,
            "texto": "¿Te sientes descansado/a al despertar?",
            "categoria": "sueño",
            "opciones": [
                {"texto": "No", "peso": 4},
                {"texto": "Más o menos", "peso": 2},
                {"texto": "Sí", "peso": 0}
            ]
        })
        
        preguntas.append({
            "id": 4,
            "texto": "Durante la noche...",
            "categoria": "sueño",
            "opciones": [
                {"texto": "Tiendo a despertarme a mitad de la noche y me cuesta conciliar nuevamente el sueño.", "peso": 4},
                {"texto": "Duermo de manera continua y sin interrupciones.", "peso": 0}
            ]
        })
        
        preguntas.append({
            "id": 5,
            "texto": "¿Mantienes un horario regular (acostarte y despertar a la misma hora)?",
            "categoria": "sueño",
            "opciones": [
                {"texto": "No", "peso": 4},
                {"texto": "Tal vez", "peso": 2},
                {"texto": "Sí", "peso": 0}
            ]
        })
        
        preguntas.append({
            "id": 6,
            "texto": "¿Cuántas tareas o proyectos tienes actualmente pendientes?",
            "categoria": "academico",
            "opciones": [
                {"texto": "0", "peso": 0},
                {"texto": "1-2", "peso": 1},
                {"texto": "3-4", "peso": 2},
                {"texto": "5-6", "peso": 3},
                {"texto": "Más de 6", "peso": 4}
            ]
        })
        
        preguntas.append({
            "id": 7,
            "texto": "¿Entregas tus tareas a tiempo?",
            "categoria": "academico",
            "opciones": [
                {"texto": "Nunca", "peso": 4},
                {"texto": "Rara vez", "peso": 3},
                {"texto": "Casi siempre", "peso": 1},
                {"texto": "Siempre", "peso": 0}
            ]
        })
        
        preguntas.append({
            "id": 8,
            "texto": "¿Qué tan exigentes consideras a tus profesores?",
            "categoria": "academico",
            "opciones": [
                {"texto": "Nada exigentes", "peso": 0},
                {"texto": "1", "peso": 1},
                {"texto": "2", "peso": 2},
                {"texto": "3 (Muy exigentes)", "peso": 3}
            ]
        })
        
        preguntas.append({
            "id": 9,
            "texto": "Mi rendimiento académico es...",
            "categoria": "academico",
            "opciones": [
                {"texto": "Malo", "peso": 4},
                {"texto": "Regular", "peso": 2},
                {"texto": "Bueno", "peso": 0}
            ]
        })
        
        preguntas.append({
            "id": 10,
            "texto": "¿Cuántas horas estudias fuera de clases diariamente?",
            "categoria": "academico",
            "opciones": [
                {"texto": "0 hrs", "peso": 0},
                {"texto": "1-2 hrs", "peso": 1},
                {"texto": "3-4 hrs", "peso": 2},
                {"texto": "5 o más hrs", "peso": 3}
            ]
        })
        
        preguntas.append({
            "id": 11,
            "texto": "¿Sientes presión por obtener buenas calificaciones?",
            "categoria": "academico",
            "opciones": [
                {"texto": "No", "peso": 0},
                {"texto": "Más o menos", "peso": 2},
                {"texto": "Normal", "peso": 2},
                {"texto": "Mucha", "peso": 4}
            ]
        })
        
        preguntas.append({
            "id": 12,
            "texto": "¿Con qué frecuencia te sientes abrumado/a por tus responsabilidades?",
            "categoria": "emocional",
            "opciones": [
                {"texto": "Nunca", "peso": 0},
                {"texto": "Rara vez", "peso": 1},
                {"texto": "Frecuentemente", "peso": 3},
                {"texto": "Siempre", "peso": 4}
            ]
        })
        
        preguntas.append({
            "id": 13,
            "texto": "¿Te cuesta concentrarte en tus estudios?",
            "categoria": "emocional",
            "opciones": [
                {"texto": "No", "peso": 0},
                {"texto": "Más o menos", "peso": 2},
                {"texto": "Sí", "peso": 4}
            ]
        })
        
        preguntas.append({
            "id": 14,
            "texto": "¿Con qué frecuencia te sientes irritable o de mal humor sin razón aparente?",
            "categoria": "emocional",
            "opciones": [
                {"texto": "Nunca", "peso": 0},
                {"texto": "Rara vez", "peso": 1},
                {"texto": "A veces", "peso": 2},
                {"texto": "Casi siempre", "peso": 3},
                {"texto": "Siempre", "peso": 4}
            ]
        })
        
        preguntas.append({
            "id": 15,
            "texto": "¿Sufres dolores de cabeza, tensión muscular o fatiga constante?",
            "categoria": "emocional",
            "opciones": [
                {"texto": "Nunca", "peso": 0},
                {"texto": "A veces", "peso": 2},
                {"texto": "Siempre", "peso": 4}
            ]
        })
        
        preguntas.append({
            "id": 16,
            "texto": "¿Te sientes capaz de manejar tus problemas emocionales por ti mismo/a?",
            "categoria": "emocional",
            "opciones": [
                {"texto": "Totalmente incapaz", "peso": 4},
                {"texto": "Algo incapaz", "peso": 3},
                {"texto": "Neutral", "peso": 2},
                {"texto": "Capaz", "peso": 1},
                {"texto": "Muy capaz", "peso": 0}
            ]
        })
        
        preguntas.append({
            "id": 17,
            "texto": "¿Has perdido interés en actividades que antes disfrutabas?",
            "categoria": "emocional",
            "opciones": [
                {"texto": "Sí", "peso": 4},
                {"texto": "No", "peso": 0}
            ]
        })
        
        preguntas.append({
            "id": 18,
            "texto": "En tu casa, ¿Cómo considerarías tu ambiente familiar?",
            "categoria": "familiar",
            "opciones": [
                {"texto": "Malo", "peso": 4},
                {"texto": "Regular", "peso": 2},
                {"texto": "Bueno", "peso": 0}
            ]
        })
        
        preguntas.append({
            "id": 19,
            "texto": "¿Recibes apoyo emocional de tu familia para tus estudios?",
            "categoria": "familiar",
            "opciones": [
                {"texto": "Nunca", "peso": 4},
                {"texto": "Rara vez", "peso": 3},
                {"texto": "A veces", "peso": 2},
                {"texto": "Frecuentemente", "peso": 1},
                {"texto": "Siempre", "peso": 0}
            ]
        })
        
        preguntas.append({
            "id": 20,
            "texto": "¿Cuáles de estas opciones describen mejor tu entorno familiar?",
            "categoria": "familiar",
            "opciones": [
                {"texto": "Gritos, peleas, golpes, abusos verbales.", "peso": 4},
                {"texto": "Gritos y peleas.", "peso": 3},
                {"texto": "Discusiones.", "peso": 2}
            ]
        })
        
        preguntas.append({
            "id": 21,
            "texto": "¿Actualmente trabajas mientras estudias?",
            "categoria": "trabajo",
            "opciones": [
                {"texto": "No trabajo", "peso": 0},
                {"texto": "Sí, solo fines de semana", "peso": 1},
                {"texto": "Trabajos ocasionales o freelance", "peso": 2},
                {"texto": "Sí, medio tiempo", "peso": 3},
                {"texto": "Sí, tiempo completo", "peso": 4}
            ]
        })
        
        preguntas.append({
            "id": 22,
            "texto": "¿Participas en actividades extracurriculares (deportes, arte, voluntariado, etc.)?",
            "categoria": "trabajo",
            "opciones": [
                {"texto": "Ninguna", "peso": 0},
                {"texto": "1 actividad", "peso": 1},
                {"texto": "2 actividades", "peso": 2},
                {"texto": "3 o más", "peso": 3}
            ]
        })
        
        preguntas.append({
            "id": 23,
            "texto": "¿Cómo manejas el estrés actualmente?",
            "categoria": "trabajo",
            "opciones": [
                {"texto": "No lo manejo, me siento desbordado/a", "peso": 4},
                {"texto": "Mal, uso métodos poco saludables (comer en exceso, aislamiento)", "peso": 3},
                {"texto": "Regular, a veces hago algo pero no es suficiente", "peso": 2},
                {"texto": "Bien, tengo algunas técnicas (respiración, ejercicio)", "peso": 1},
                {"texto": "Muy bien, uso técnicas efectivas (meditación, deporte, terapia)", "peso": 0}
            ]
        })
        
        return preguntas
    
    def obtener_preguntas(self):
    
        return [
            {
                "id": p["id"],
                "texto": p["texto"],
                "categoria": p["categoria"],
                "opciones": [{"texto": opt["texto"]} for opt in p["opciones"]]
            }
            for p in self.cuestionario["preguntas"]
        ]
    
    def calcular_nivel_estres(self, respuestas_usuario):
       
        puntaje_obtenido = 0
        puntaje_maximo_posible = 0
        
        for pregunta in self.cuestionario["preguntas"]:
            id_preg = pregunta["id"]
            opciones = pregunta["opciones"]
            

            max_peso = max([opt["peso"] for opt in opciones])
            puntaje_maximo_posible += max_peso
            
            
            if id_preg in respuestas_usuario:
                idx_respuesta = respuestas_usuario[id_preg]
                
                if 0 <= idx_respuesta < len(opciones):
                    puntaje_obtenido += opciones[idx_respuesta]["peso"]
                else:
                    
                    puntaje_obtenido += max_peso
            else:
                
                puntaje_obtenido += max_peso
        
       
        if puntaje_maximo_posible > 0:
            nivel_estres = (puntaje_obtenido / puntaje_maximo_posible) * 10
        else:
            nivel_estres = 0
        
        
        if nivel_estres <= 2.5:
            categoria = "Bajo"
            color = "success"
            recomendacion = "¡Muy bien! Mantén tus hábitos saludables. Sigue así."
        elif nivel_estres <= 5:
            categoria = "Moderado"
            color = "info"
            recomendacion = "Estrés normal. Sigue con tus buenas prácticas y cuida tu descanso."
        elif nivel_estres <= 7.5:
            categoria = "Alto"
            color = "warning"
            recomendacion = "Tu nivel de estrés es alto. Considera ajustar tu rutina y pedir apoyo."
        else:
            categoria = "Muy Alto"
            color = "danger"
            recomendacion = "Tu estrés es muy alto. Es importante que busques apoyo profesional (psicólogo o consejero escolar)."
        
        return {
            "puntuacion": round(nivel_estres, 1),
            "categoria": categoria,
            "color": color,
            "recomendacion_principal": recomendacion,
            "puntaje_total": puntaje_obtenido,
            "puntaje_maximo": puntaje_maximo_posible
        }



    