from flask import Flask, render_template, request, url_for
from SimplexMethodLPPSolver.main import bp
import json
from SimplexMethodLPPSolver import simplex
from simplexGraphic import plot_linear_programming_problem
from simplexGraphicAlt import plot_linear_programming_problem_alt
import re

app = Flask(__name__)
app.register_blueprint(bp)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/inicio', methods=['POST'])
def inicio():
    global const
    global var
    const = int(request.form.get('const'))
    var = int(request.form.get('var'))

    return render_template('index.html', content=render_template('restricao.html', var=var, const=const))

@app.route('/calcular', methods=['POST'])
def calcular():
    global type
    global objective_expression
    global constraint_expressions
    
    type = request.form.get('type')
    objective_expression = request.form.get('objective_expression')
    constraint_expressions = json.loads(request.form.get('constraint_expressions'))
    

    simplex(type, objective_expression, constraint_expressions)
    
    return render_template('index.html', content2=render_template('inicioResultado.html', objective_expression=objective_expression, constraint_expressions=constraint_expressions, const = const, type=type))


@app.route('/grafico', methods=['POST'])
def grafico():
    
    def possui_igualdade(expressoes):
        padrao = r'^[^<>=]*='
        for expressao in expressoes:
            if re.match(padrao, expressao):
                return True
        return False


    resultado = possui_igualdade(constraint_expressions)
    if(resultado):
        # Para restricoes que possuam =, alem >= ou <=
        plot_linear_programming_problem(objective_expression, constraint_expressions, type)
    else:
        # Para restricoes que nao possuam =, apenas >= ou <=
        plot_linear_programming_problem_alt(objective_expression, constraint_expressions, type)
        
    return render_template('index.html', content2=render_template('inicioResultado.html', objective_expression=objective_expression, constraint_expressions=constraint_expressions, const = const, type=type))



if __name__ == '__main__':
    app.run(debug=True)