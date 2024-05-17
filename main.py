from flask import Flask, redirect, url_for, request, render_template, make_response

import game

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def start():
    if request.method == 'POST':
        return redirect(url_for('play_get'))
    
    #get high score
    high_score = request.cookies.get("high_score")
    if high_score == None:
        high_score = 0
     
    return render_template('home.html', high_score = high_score)

@app.get('/play')
def play_get():    
    grid = request.cookies.get("state")
    score = request.cookies.get("score")
    if score == None:
        score = 0
    #if there is no grid loaded create a new one
    if grid == None:
        grid_list =game.create_grid()
        esp = make_response(render_template('2048.html',grid = grid_list, score = 0))
        esp.set_cookie("state",game.gridToJson(grid_list))
        return esp
    #if there is a grid loaded load the layout of that grid
    grid_list = game.jsonToGrid(grid)
    score = request.cookies.get("score")
    if score == None:
        score = "0"
    else:
        score = score
    esp = make_response(render_template('2048.html',grid = grid_list, score = score))
    return esp
@app.post('/play')
def play_post():
    grid_list = game.jsonToGrid(request.cookies.get("state"))
    score = request.cookies.get("score")
    if score == None:
        score = 0
    else:
        score = int(score)
    high_score = request.cookies.get("high_score")
    if high_score == None:
        high_score = 0
    else:
        high_score = int(high_score)
    game_state = game.game_state(grid_list,score)
    if request.form["control"] == "Left":
        game_state = game.left(game_state)
    elif request.form["control"] == "Right":
        game_state = game.right(game_state)
    elif request.form["control"] == "Up":
        game_state = game.up(game_state)
    elif request.form["control"] == "Down":
        game_state = game.down(game_state)

    elif request.form["control"] == "Quit":
        esp = make_response(redirect(url_for("start")))
        esp.delete_cookie("state")
        esp.delete_cookie("score")
        if high_score == None or score > high_score: 
            esp.set_cookie("high_score",str(score))
        return esp
    
    #if player has won or lost move them to that path
    if game_state.state == game.state.win:
        esp = make_response(redirect(url_for('win',score = score)))
        esp.delete_cookie("state")
        esp.delete_cookie("score")
        if high_score == None or score > high_score: 
            esp.set_cookie("high_score",str(score))
        return esp
    elif game_state.state == game.state.lost:
        esp = make_response(redirect(url_for('lost',score = score)))
        esp.delete_cookie("state")
        esp.delete_cookie("score")
        if high_score == None or score > high_score: 
            esp.set_cookie("high_score",str(score))
        return esp

    esp = make_response(render_template('2048.html',grid = game_state.grid, score = game_state.score))
    esp.set_cookie("state",game.gridToJson(game_state.grid))
    esp.set_cookie("score",str(game_state.score))
    return esp


@app.route('/win?score=<score>', methods=['POST', 'GET'])
def win(score: int):
    if request.method == "GET":
        return render_template('win.html', score = score)
    
    return redirect(url_for('start'))

@app.route('/lost?score=<score>', methods=['POST', 'GET'])
def lost(score: int):
    if request.method == "GET":
        return render_template('lost.html', score = score)
    
    return redirect(url_for('start'))


if __name__ == '__main__':
    app.run(debug=True)
