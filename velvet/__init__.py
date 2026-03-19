import os, typing, tkinter as tk


type Rank = typing.Literal["2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k", "a"]
type Suit = typing.Literal["c", "d", "h", "s"]

YES_VALUES: list[str] = ["y", "yes", "yeah", "v"]
NO_VALUES: list[str] = ["n", "no", "nope", "x"]

def notationToRank(rank_char: str) -> str | None:
    if rank_char.isdigit() and 1 < int(rank_char) < 11:
        return rank_char
    return {
        "j": "Jack",
        "q": "Queen",
        "k": "King",
        "a": "Ace"
    }.get(rank_char.lower())

def notationToSuit(suit_char: str) -> str | None:
    return {
        "c": "Clubs",
        "d": "Diamonds",
        "h": "Hearts",
        "s": "Spades"
    }.get(suit_char.lower())

class Joker:
    def getString(self) -> str:
        return "Joker"
class GoldenKing:
    def getString(self) -> str:
        return "Golden King"
class Card:
    def __init__(self, rank: Rank, suit: Suit) -> None:
        self.rank: Rank = rank
        self.suit: Suit = suit
    @classmethod
    def fromNotation(cls, notation: str) -> "Card | Joker | GoldenKing | str":
        rank: Rank | None = None
        suit: Suit | None = None
        notation = notation.lower().strip()
        if not notation:
            return "please enter a card."
        if notation == "j":
            return Joker()
        if notation == "gk":
            return GoldenKing()
        if not notation.startswith("10") and notation[0] not in "23456789jqka":
            return "invalid rank."
        if not notation[1:]:
            return f"{notation[0]} of..?"
        if notation.startswith("10"):
            rank = "10"
            if not notation[2:]:
                return f"10 of..?"
            if notation[2] in "cdhs":
                suit = notation[2] # type: ignore
            else:
                return "invalid rank."
        if not rank:
            if notation[0] in "23456789jqka":
                rank = notation[0] # type: ignore
            else:
                return "invalid rank."
        if not suit:
            if notation[1] in "cdhs" and not suit:
                suit = notation[1] # type: ignore
            else:
                return "invalid suit."
        return cls(rank, suit) # type: ignore

    def getString(self) -> str:
        return f"{notationToRank(self.rank)} of {notationToSuit(self.suit)}"

class VelvetLustre:
    def __init__(self, *players: str) -> None:
        self.tk: tk.Tk = tk.Tk()
        self.tk.withdraw()
        self.players: dict[str, dict[str, typing.Any]] = {player: {
            "stack": []
        } for player in players}
    def openPrompt(self) -> None:
        setup_tk: tk.Toplevel = tk.Toplevel()
        setup_tk.title("velvet | setup")
        setup_tk.geometry("1000x500")
        for player in self.players:
            label: tk.Label = tk.Label(
                setup_tk,
                text=f"{player}, please enter all 16 cards in your stack. examples:\n"
                f"  2s for two of spades,\n"
                f"  10h for ten of hearts,\n"
                f"  kd for king of diamonds,\n"
                f"  j for joker,\n"
                f"  gk for golden king\n",
                font=("arial", 20)
            )
            label.pack()
            entry: tk.Entry = tk.Entry(setup_tk, width=300)
            card_num: int = 1
            def submit() -> None:
                card: Card | Joker | GoldenKing | str = Card.fromNotation(entry.get())
                os.system("cls" if os.name == "nt" else "clear")
                if isinstance(card, str):
                    label.config(text=card)
                else:
                    self.players[player]["stack"].append(card)
                    label.config(text=f"added {card.getString()}.")
                    entry.delete(0, tk.END)
            tk.Button(setup_tk, text="confirm")
            while True:
                if len(self.players[player]["stack"]) == 16:
                    break

        while True:
            for player in self.players:
                print(f"{player}'{'' if player.endswith('s') else 's'} turn")