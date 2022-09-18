#!/usr/bin/env python3

import sys, time, random, select, termios

class Snake:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows

        # Hide Cursor
        print("\x1b[?25l", end='')

        self.oldt = termios.tcgetattr(sys.stdout.fileno())
        newt = [i for i in self.oldt]
        newt[3] = newt[3] & ~(termios.ECHO | termios.ICANON)
        termios.tcsetattr(sys.stdout.fileno(), termios.TCSANOW, newt)

    def __del__(self):
        # Show cursor
        print("\x1b[?25h", end='')
        termios.tcsetattr(sys.stdout.fileno(), termios.TCSANOW, self.oldt)

    def _print_at(self, x, y, c):
        print("\x1b[%iB\x1b[%iC%s" % (y + 1, x + 1, c), end='')
        print("\x1b[%iF" % (y + 1), end='')

    def run(self):
        x, y = [0] * 1024, [0] * 1024
        while True:
            # Render field
            print("┌" + "─" * self.cols + "┐")
            for _ in range(self.rows):
                print("│" + "·" * self.cols + "│")
            print("└" + "─" * self.cols + "┘")
            print("\x1b[%iA" % (self.rows + 2), end='')

            head, tail = 0, 0
            x[head], y[head] = self.cols / 2, self.rows / 2
            gameover = False
            xdir, ydir = 1, 0
            applex, appley = None, None

            while not gameover:
                if applex == None:
                    # Create new apple
                    applex, appley = random.randrange(self.cols), random.randrange(self.rows)
                    i = tail
                    while i != head:
                        if x[i] == applex and y[i] == appley:
                            applex = None
                        i = (i + 1) & 1023
                    # Draw apple
                    if applex != None:
                        self._print_at(applex, appley, '❤')

                # Clear snake tail
                self._print_at(x[tail], y[tail], '·')

                if x[head] == applex and y[head] == appley:
                    applex = None
                else:
                    tail = (tail + 1) & 1023

                newhead = (head + 1) & 1023
                x[newhead] = (x[head] + xdir) % self.cols
                y[newhead] = (y[head] + ydir) % self.rows
                head = newhead

                i = tail
                while i != head:
                    if x[i] == x[head] and y[i] == y[head]:
                        gameover = True
                    i = (i + 1) & 1023

                # Draw snake head
                self._print_at(x[head], y[head], '▓')
                sys.stdout.flush()
                time.sleep(5 * 1.0 / 60)

                inp, _, _ = select.select([sys.stdin], [], [], 0)
                if len(inp) > 0:
                    c = sys.stdin.read(1)
                    if c == '\x1b' or c == 'q':
                        return
                    if c == 'h' and xdir != 1:
                        xdir, ydir = -1, 0
                    elif c == 'l' and xdir != -1:
                        xdir, ydir = 1, 0
                    elif c == 'j' and ydir != -1:
                        xdir, ydir = 0, 1
                    elif c == 'k' and ydir != 1:
                        xdir, ydir = 0, -1

            # Gameover
            self._print_at(self.cols / 2 - 5, self.rows / 2, " Game Over! ")
            sys.stdout.flush()
            sys.stdin.read(1)

if __name__ == "__main__":
    Snake(60, 30).run()

