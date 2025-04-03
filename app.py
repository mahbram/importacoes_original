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
        return '<h1>Por favor, envie ambos os arquivos: base e template.</h1>'

    try:
        # Salva os arquivos temporariamente
        base_path = os.path.join(app.config['UPLOAD_FOLDER'], "base.xlsx")
        template_path = os.path.join(app.config['UPLOAD_FOLDER'], "template.xlsx")

        base.save(base_path)
        template.save(template_path)

        # Processa os arquivos
        dados_filtrados = ler_centros_custo(base_path)
        if not dados_filtrados:
            return '<h1>Nenhum dado válido encontrado na base.</h1>'

        caminho_saida = preencher_template(template_path, dados_filtrados, grupo)

        # Retorna o arquivo processado para download
        return send_file(caminho_saida, as_attachment=True)
    except Exception as e:
        return f'<h1>Erro: {e}</h1>'
    finally:
        # Remove os arquivos temporários
        for file in [base_path, template_path, "template_atualizado.xlsx"]:
            if os.path.exists(file):
                try:
                    os.remove(file)
                except PermissionError:
                    pass

# Rota para processar formulário
@app.route('/submit_form', methods=['POST'])
def submit_form():
    titulo = request.form.get('titulo')
    codigo = request.form.get('codigo')
    aplicacao = request.form.get('aplicacao')
    descricao = request.form.get('descricao')

    # Exemplo de processamento (pode ser substituído por lógica de banco de dados)
    print(f"Título: {titulo}")
    print(f"Código: {codigo}")
    print(f"Aplicação: {aplicacao}")
    print(f"Descrição: {descricao}")

    return "Formulário enviado com sucesso!"

# Rota para obter dados de uma planilha
@app.route('/obter_dados_planilha', methods=['GET'])
def obter_dados_planilha():
    caminho_planilha = os.path.join(app.config['UPLOAD_FOLDER'], "TemplateCargaGrupos_Novo.xlsx")
    try:
        wb = load_workbook(caminho_planilha, data_only=True)
        ws = wb.active

        dados = {
            "colunaA": ws["A7"].value,
            "colunaB": ws["B7"].value,
            "colunaC": ws["C7"].value,
            "colunaD": ws["D7"].value,
        }

        return jsonify(dados)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Rota para obter um sequencial
@app.route('/obter_sequencial', methods=['GET'])
def obter_sequencial():
    sequencial = 123  # Exemplo de valor sequencial
    return jsonify({'sequencial': sequencial})

# Configurações do Flask
app.config['UPLOAD_FOLDER'] = 'uploads/'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)