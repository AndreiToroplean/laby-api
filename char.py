from dirs import Dirs


class Char:
    _H_LEN = 4

    START = '←┼→'
    FINISH = '→┼←'

    H_SPACE = ' ' * _H_LEN
    H_WALL = '─' * _H_LEN
    V_SPACE = ' '
    V_WALL = '│'

    NONE_CORNER = ' '
    L_CORNER = '╴'
    R_CORNER = '╶'
    U_CORNER = '╵'
    D_CORNER = '╷'
    LR_CORNER = '─'
    UD_CORNER = '│'
    RD_CORNER = '┌'
    LD_CORNER = '┐'
    RU_CORNER = '└'
    LU_CORNER = '┘'
    LRU_CORNER = '┴'
    LRD_CORNER = '┬'
    RUD_CORNER = '├'
    LUD_CORNER = '┤'
    LRUD_CORNER = '┼'

    CORNER = {
        Dirs.NONE: NONE_CORNER,
        Dirs.LEFT: L_CORNER,
        Dirs.RIGHT: R_CORNER,
        Dirs.UP: U_CORNER,
        Dirs.DOWN: D_CORNER,
        Dirs.LEFT | Dirs.RIGHT: LR_CORNER,
        Dirs.UP | Dirs.DOWN: UD_CORNER,
        Dirs.RIGHT | Dirs.DOWN: RD_CORNER,
        Dirs.LEFT | Dirs.DOWN: LD_CORNER,
        Dirs.RIGHT | Dirs.UP: RU_CORNER,
        Dirs.LEFT | Dirs.UP: LU_CORNER,
        Dirs.LEFT | Dirs.RIGHT | Dirs.UP: LRU_CORNER,
        Dirs.LEFT | Dirs.RIGHT | Dirs.DOWN: LRD_CORNER,
        Dirs.RIGHT | Dirs.UP | Dirs.DOWN: RUD_CORNER,
        Dirs.LEFT | Dirs.UP | Dirs.DOWN: LUD_CORNER,
        Dirs.LEFT | Dirs.RIGHT | Dirs.UP | Dirs.DOWN: LRUD_CORNER,
    }
