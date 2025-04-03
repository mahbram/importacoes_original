from flask import Flask, render_template, request, send_file, jsonify
from utils import ler_centros_custo, preencher_template
import os

app = Flask(__name__)

# Página inicial para upload de arquivos
@app.route('/')
def upload():
    return render_template('upload.html')

# Rota para processar o upload dos arquivos
@app.route('/upload', methods=['POST'])
def upload_file():
    base = request.files.get('base')
    template = request.files.get('template')
    grupo = request.form.get('grupo')

    if not base or not template:
        return jsonify({"erro": "Por favor, envie ambos os arquivos: base e template."}), 400

    try:
        # Salva os arquivos temporariamente
        base_path = os.path.join(app.config['UPLOAD_FOLDER'], "base.xlsx")
        template_path = os.path.join(app.config['UPLOAD_FOLDER'], "template.xlsx")

        base.save(base_path)
        template.save(template_path)

        # Processa os arquivos
        dados_filtrados = ler_centros_custo(base_path)
        if not dados_filtrados:
            return jsonify({"erro": "Nenhum dado válido encontrado na base."}), 400

        caminho_saida = preencher_template(template_path, dados_filtrados, grupo)

        # Retorna o arquivo processado para download
        return send_file(caminho_saida, as_attachment=True)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        # Remove os arquivos temporários
        for file in [base_path, template_path, "template_atualizado.xlsx"]:
            if os.path.exists(file):
                try:
                    os.remove(file)
                except PermissionError:
                    pass

# Rota para obter o próximo sequencial
@app.route('/obter_sequencial', methods=['GET'])
def obter_sequencial():
    # Exemplo de lógica para obter o próximo sequencial
    ultimo_grupo = 100  # Substitua por lógica real
    proximo_grupo = ultimo_grupo + 1
    return jsonify({
        "ultimo_grupo": ultimo_grupo,
        "proximo_grupo": proximo_grupo
    })

# Rota para salvar um novo grupo
@app.route('/salvar_grupo', methods=['POST'])
def salvar_grupo():
    dados = request.json
    titulo = dados.get('titulo')
    codigo = dados.get('codigo')
    descricao = dados.get('descricao')

    if not titulo or not codigo or not descricao:
        return jsonify({"erro": "Preencha todos os campos obrigatórios!"}), 400

    # Aqui você pode adicionar a lógica para salvar o grupo no banco de dados
    print(f"Novo grupo salvo: {titulo}, {codigo}, {descricao}")

    return jsonify({"mensagem": "Grupo criado com sucesso!"})

# Configurações do Flask
app.config['UPLOAD_FOLDER'] = 'uploads/'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)