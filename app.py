from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Configurações do banco de dados PostgreSQL
db_host = 'localhost'
db_port = '5432'
db_name = 'academia'
db_user = 'postgres'
db_password = '123'

# Função para conectar ao banco de dados
def connect_db():
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )
    return conn

# Rota para exibir o formulário de cadastro de aluno
@app.route('/')
def index():
    return render_template('index.html')

# Rota para cadastrar aluno no banco de dados
@app.route('/cadastrar_aluno', methods=['POST'])
def cadastrar_aluno():
    conn = connect_db()
    cursor = conn.cursor()

    # Receber dados do formulário
    nome = request.form['nome']
    data_nasc = request.form['data_nasc']
    endereco = request.form['endereco']
    telefone = request.form['telefone']
    email = request.form['email']
    data_inicio = request.form['data_inicio']
    status = request.form['status']

    # Executar o INSERT no banco de dados
    cursor.execute("""
        INSERT INTO Aluno (Nome, DataNasc, Endereco, Telefone, Email, DataInicio, Status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (nome, data_nasc, endereco, telefone, email, data_inicio, status))

    conn.commit()

    # Fechar cursor e conexão
    cursor.close()
    conn.close()

    return redirect(url_for('outra_tela'))

# Rota para editar aluno
@app.route('/editar_aluno/<int:aluno_id>', methods=['GET', 'POST'])
def editar_aluno(aluno_id):
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == 'GET':
        # Selecionar os dados do aluno pelo ID para preencher o formulário de edição
        cursor.execute("SELECT * FROM Aluno WHERE ID_Aluno = %s", (aluno_id,))
        aluno = cursor.fetchone()
        cursor.close()
        conn.close()
        if aluno:
            return render_template('editar_aluno.html', aluno=aluno)
        else:
            return "Aluno não encontrado."

    elif request.method == 'POST':
        # Receber os novos dados do formulário de edição
        nome = request.form['nome']
        data_nasc = request.form['data_nasc']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        email = request.form['email']
        data_inicio = request.form['data_inicio']
        status = request.form['status']

        # Executar o UPDATE no banco de dados
        cursor.execute("""
            UPDATE Aluno
            SET Nome = %s, DataNasc = %s, Endereco = %s, Telefone = %s, Email = %s,
                DataInicio = %s, Status = %s
            WHERE ID_Aluno = %s;
        """, (nome, data_nasc, endereco, telefone, email, data_inicio, status, aluno_id))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('outra_tela'))

# Rota para excluir aluno
@app.route('/excluir_aluno/<int:aluno_id>', methods=['GET', 'POST'])
def excluir_aluno(aluno_id):
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == 'GET':
        # Selecionar os dados do aluno pelo ID para exibição antes da exclusão
        cursor.execute("SELECT * FROM Aluno WHERE ID_Aluno = %s", (aluno_id,))
        aluno = cursor.fetchone()
        cursor.close()
        conn.close()
        if aluno:
            return render_template('confirmar_exclusao.html', aluno=aluno)
        else:
            return "Aluno não encontrado."

    elif request.method == 'POST':
        # Executar o DELETE no banco de dados
        cursor.execute("DELETE FROM Aluno WHERE ID_Aluno = %s", (aluno_id,))
        conn.commit()
        cursor.close()
        conn.close()

        # Verificar se ainda há alunos restantes
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Aluno")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        if count == 0:
            return redirect(url_for('index'))
        else:
            return redirect(url_for('outra_tela'))

# Rota para a outra tela
@app.route('/outra_tela')
def outra_tela():
    conn = connect_db()
    cursor = conn.cursor()

    # Selecionar todos os alunos
    cursor.execute("SELECT * FROM Aluno")
    alunos = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('outra_tela.html', alunos=alunos)

if __name__ == '__main__':
    app.run(debug=True)
