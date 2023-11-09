# the main function of the game

if __name__ == "__main__":
    from src import init_game, run_game

    game = init_game("./assets/init.yaml")
    run_game(game)
