#!/usr/bin/env python3

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
# Disable CORS since frontend and backend are same-origin
# CORS not needed for same-origin requests

# Configure OpenAI client
client = OpenAI()  # Automatically reads OPENAI_API_KEY from environment

# Prompts especializados para cada tipo de cálculo
PROMPT_TEMPLATES = {
    'basico': "Você é um assistente de matemática básica. Calcule expressões aritméticas simples. Retorne apenas o resultado numérico final, sem explicações.",
    'algebra': "Você é um assistente de álgebra. Resolva equações, simplifique expressões algébricas e trabalhe com variáveis. Se resolver uma equação, retorne a solução no formato 'x = valor'. Se simplificar, retorne a expressão simplificada. Sem passos, apenas o resultado final.",
    'calculo': "Você é um assistente de cálculo. Calcule derivadas, integrais e limites. Use notação matemática padrão. Para integrais indefinidas, inclua '+ C'. Retorne apenas o resultado final, sem passos.",
    'geometria': "Você é um assistente de geometria. Calcule áreas, perímetros, volumes e outras medidas geométricas usando as fórmulas apropriadas. Inclua unidades quando fornecidas. Se faltarem dados essenciais, responda 'Dados insuficientes'. Retorne apenas o valor final com unidade.",
    'estatistica': "Você é um assistente de estatística. Calcule médias, medianas, desvio padrão, probabilidades e outras medidas estatísticas. Para listas numéricas use formato (1,2,3). Arredonde resultados para 4 casas decimais quando necessário. Retorne apenas o valor final."
}

@app.route('/')
def serve_index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')


@app.route('/api/calcular', methods=['POST'])
def calcular():
    """Handle math calculations using OpenAI"""
    try:
        # Validate JSON request
        if not request.is_json:
            return jsonify({'error': 'Content-Type deve ser application/json'}), 400
            
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({'error': 'JSON inválido'}), 400
            
        pergunta = data.get('pergunta', '').strip() if isinstance(data, dict) else ''
        tipo = data.get('tipo', 'basico').lower() if isinstance(data, dict) else 'basico'
        
        # Input validation
        if not pergunta:
            return jsonify({'error': 'Pergunta não fornecida'}), 400
            
        if len(pergunta) > 1000:
            return jsonify({'error': 'Pergunta muito longa (máximo 1000 caracteres)'}), 400
            
        # Validate calculation type
        if tipo not in PROMPT_TEMPLATES:
            valid_types = ', '.join(PROMPT_TEMPLATES.keys())
            return jsonify({'error': f'Tipo inválido. Tipos válidos: {valid_types}'}), 400
        
        # Get the appropriate prompt for the calculation type
        system_prompt = PROMPT_TEMPLATES[tipo]
        
        # Log the request type for debugging
        app.logger.info(f"Calculation request - Type: {tipo}, Question: {pergunta[:50]}...")
        
        # Make the API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": system_prompt
                },
                {
                    "role": "user", 
                    "content": pergunta
                }
            ],
            temperature=0
        )
        
        resposta = response.choices[0].message.content.strip()
        return jsonify({'resposta': resposta})
        
    except Exception as e:
        # Log error for debugging
        app.logger.error(f"Error in calcular endpoint: {str(e)}")
        
        # Handle specific OpenAI errors with appropriate status codes
        error_type = type(e).__name__
        error_str = str(e).lower()
        
        if "authentication" in error_str or "401" in error_str:
            return jsonify({'error': 'Erro de autenticação da API'}), 502
        elif "rate_limit" in error_str or "429" in error_str:
            return jsonify({'error': 'Limite de requisições atingido. Tente novamente em alguns momentos.'}), 429
        elif "insufficient_quota" in error_str or "quota" in error_str:
            return jsonify({'error': 'Cota da API esgotada'}), 502
        elif "permission" in error_str or "403" in error_str:
            return jsonify({'error': 'Sem permissão para acessar a API'}), 502
        else:
            return jsonify({'error': 'Erro ao processar a solicitação. Tente novamente.'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint não encontrado'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
