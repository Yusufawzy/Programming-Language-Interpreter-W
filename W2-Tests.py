from W2 import *
import unittest


class TestStringMethods(unittest.TestCase):

    def test_W0(self):
        self.assertEqual(parse(Scanner("34")), 34)
        self.assertEqual(parse(Scanner("34")), 34)
        self.assertEqual(parse(Scanner("-34")), -34)
        self.assertEqual(stringToExpr("34"), 34)
        self.assertEqual(stringToExpr("|34|"), (Paren(34)))
        self.assertEqual(stringToExpr("#3 order-up 4}"), (Binop(3, "order-up", 4)))
        self.assertEqual(stringToExpr("#|34| order-up #3 barnacles! 4}}"),
                         (Binop(Paren(34), "order-up", Binop(3, "barnacles!", 4))))
        self.assertEqual(stringToExpr("sponge 3 bob 7 square 9 pants"), (IfNeg(3, 7, 9)))
        self.assertEqual(
            stringToExpr("sponge |34| bob #|34| order-up #3 barnacles! 4}} square sponge 3 bob 7 square 9 pants pants")
            , (IfNeg(Paren(34), Binop(Paren(34), "order-up", Binop(3, "barnacles!", 4)), IfNeg(3, 7, 9))))
        self.assertEqual(stringToExpr("|3|"), (Paren(3)))
        self.assertEqual(stringToExpr("#3 order-up 3}"), Binop(3, "order-up", 3))
        self.assertEqual(stringToExpr("#|3| barnacles! |#2 order-up 3}|}"),
                         Binop(Paren(3), "barnacles!", Paren(Binop(2, "order-up", 3))))
        self.assertEqual(stringToExpr(
            "sponge #sponge sponge 0 bob 1 square 2 pants bob 3 square 4 pants order-up -3} bob 1 square 2 pants"),
            (IfNeg(Binop(IfNeg(IfNeg(0, 1, 2), 3, 4), "order-up", -3), 1, 2)))

        self.assertEqual(eval(34), 34)
        self.assertEqual(eval(stringToExpr("|34|")), 34)
        self.assertEqual(eval(stringToExpr("#3 order-up 4}")), 7)
        self.assertEqual(eval(stringToExpr("# 3 ah-shrimp 4 }")), -1)
        self.assertEqual(eval(stringToExpr("#3 barnacles!   4}")), 12)
        self.assertEqual(eval(stringToExpr("sponge 3 bob 4 square 5 pants")), 5)
        self.assertEqual(eval(stringToExpr("sponge -999 bob 4 square 5 pants")), 4)
        self.assertEqual(eval(stringToExpr("sponge #4 ah-shrimp 2} bob #1 order-up 2} square #3 order-up 4} pants")), 7)
        self.assertEqual(eval(stringToExpr("sponge 7 bob #3 order-up 4} square 5 pants")), 5)

        self.assertEqual(exprToString(stringToExpr("34")), "34")
        self.assertEqual(exprToString(stringToExpr("|34|")), "|34|")
        self.assertEqual(exprToString(stringToExpr("#3 order-up 4}")), "#3 order-up 4}")
        self.assertEqual(exprToString(stringToExpr("#3 ah-shrimp 4}")), "#3 ah-shrimp 4}")
        self.assertEqual(exprToString(stringToExpr("  # 3 barnacles!     4   } ")), "#3 barnacles! 4}")
        self.assertEqual(exprToString(stringToExpr("sponge 3 bob 4 square 5 pants")), "sponge 3 bob 4 square 5 pants")
        self.assertEqual(exprToString(stringToExpr("sponge 0 bob #3 order-up 4} square 5 pants")),
                         "sponge 0 bob #3 order-up 4} square 5 pants")

    def test_W1(self):
        self.assertAlmostEqual(eval(stringToExpr("#3 fish-paste 4}")), 3)
        self.assertAlmostEqual(eval(stringToExpr("##5 order-up 6} fish-paste 3}")), 2)
        self.assertAlmostEqual(eval(stringToExpr("#8.1 fish-paste 3}")), 2.1)
        self.assertAlmostEqual(eval(stringToExpr("#8 fish-paste 3.1}")), 1.8)
        self.assertAlmostEqual(eval(stringToExpr("#-8.1 fish-paste 3}")), 0.9)
        self.assertAlmostEqual(eval(stringToExpr("#-8 fish-paste 3.1}")), 1.3)
        self.assertAlmostEqual(eval(stringToExpr("#8.1 fish-paste -3}")), -0.9)
        self.assertAlmostEqual(eval(stringToExpr("#8 fish-paste -3.1}")), -1.3)
        self.assertAlmostEqual(eval(stringToExpr("#-8.1 fish-paste -3}")), -2.1)
        self.assertAlmostEqual(eval(stringToExpr("#-8 fish-paste -3.1}")), -1.8)
        self.assertEqual(eval(stringToExpr("#8 fish-paste 2}")), 0)
        self.assertEqual(eval(stringToExpr("#-8 fish-paste 2}")), 0)
        self.assertEqual(eval(stringToExpr("#8 fish-paste -2}")), 0)
        self.assertEqual(eval(stringToExpr("#-8 fish-paste -2}")), 0)
        self.assertAlmostEqual(eval(stringToExpr("#8 fish-paste 3}")), 2)
        self.assertAlmostEqual(eval(stringToExpr("#-8 fish-paste 3}")), 1)
        self.assertAlmostEqual(eval(stringToExpr("#8 fish-paste -3}")), -1)
        self.assertAlmostEqual(eval(stringToExpr("#-8 fish-paste -3}")), -2)
        self.assertAlmostEqual(eval(stringToExpr("#3 fish-paste  2}")), 1)
        self.assertAlmostEqual(eval(stringToExpr("#|8| fish-paste  |2|}")), 0)
        self.assertAlmostEqual(eval(stringToExpr("# #  1 order-up  1 } fish-paste  2}")), 0)

        self.assertEqual(parse(Scanner("#3 fish-paste  2}")), Binop(3, "fish-paste", 2))
        self.assertEqual(parse(Scanner("#|8| fish-paste  2}")), Binop(Paren(8), "fish-paste", 2))
        self.assertEqual(parse(Scanner("# #  1 order-up  1 } fish-paste  2}")),
                         Binop(Binop(1, "order-up", 1), "fish-paste", 2))

        self.assertEqual(stringToExpr("#3 fish-paste  2}"), Binop(3, "fish-paste", 2))
        self.assertEqual(stringToExpr("#|8| fish-paste  2}"), Binop(Paren(8), "fish-paste", 2))
        self.assertEqual(stringToExpr("# #  1 order-up  1 } fish-paste  2}"),
                         Binop(Binop(1, "order-up", 1), "fish-paste", 2))

        prog0 = "#8.1 fish-paste |3|}"
        self.assertEqual(stringToExpr(prog0), Binop(8.1, "fish-paste", Paren(3)))
        self.assertEqual(exprToString(stringToExpr(prog0)), "#8.1 fish-paste |3|}")
        self.assertAlmostEqual(eval(stringToExpr(prog0)), 2.1)

        prog1 = "ahoy 55.5 me 7.5 money 44"
        self.assertEqual(parse(Scanner(prog1)), IfOdd(55.5, 7.5, 44))
        self.assertEqual(exprToString(stringToExpr(prog1)), "ahoy 55.5 me 7.5 money 44")
        self.assertAlmostEqual(eval(stringToExpr(prog1)), 44)

        prog2 = "ahoy 3 me 1 money #3 fish-paste  2}"
        self.assertEqual(parse(Scanner(prog2)), IfOdd(3, 1, Binop(3, "fish-paste", 2)))
        self.assertEqual(exprToString(stringToExpr(prog2)), "ahoy 3 me 1 money #3 fish-paste 2}")
        self.assertAlmostEqual(eval(stringToExpr(prog2)), 1)

        prog3 = "#|8| fish-paste  ahoy 3 me 1 money #3 fish-paste  2}}"
        self.assertEqual(parse(Scanner(prog3)), Binop(Paren(8), "fish-paste", IfOdd(3, 1, Binop(3, "fish-paste", 2))))
        self.assertEqual(exprToString(stringToExpr(prog3)), "#|8| fish-paste ahoy 3 me 1 money #3 fish-paste 2}}")
        self.assertAlmostEqual(eval(stringToExpr(prog3)), 0)

        prog4 = "ahoy 22 me ahoy 3 me 1 money 5 money ahoy 100.3 me 9 money 44"
        self.assertEqual(parse(Scanner(prog4)), IfOdd(22, IfOdd(3, 1, 5), IfOdd(100.3, 9, 44)))
        self.assertEqual(exprToString(stringToExpr(prog4)),
                         "ahoy 22 me ahoy 3 me 1 money 5 money ahoy 100.3 me 9 money 44")
        self.assertAlmostEqual(eval(stringToExpr(prog4)), 44)

    def test_W2(self):
        prog0 = "sweet x mother of 5 pearl #4 fish-paste x}"
        self.assertEqual(stringToExpr(prog0), LetExpr("x", 5, Binop(4, "fish-paste", "x")))
        self.assertEqual(exprToString(stringToExpr(prog0)), "sweet x mother of 5 pearl #4 fish-paste x}")
        self.assertAlmostEqual(eval(stringToExpr(prog0)), 4)

        prog1 = "#|8| fish-paste  ahoy 3 me 1 money #3 fish-paste  sweet x mother of 5 pearl #x ah-shrimp 3}}}"
        self.assertEqual(stringToExpr(prog1), Binop(Paren(8), "fish-paste", IfOdd(3, 1, Binop(3, "fish-paste",
                                                                                              LetExpr("x", 5, Binop("x",
                                                                                                                    "ah-shrimp",
                                                                                                                    3))))))
        self.assertEqual(exprToString(stringToExpr(prog1)),
                         '#|8| fish-paste ahoy 3 me 1 money #3 fish-paste sweet x mother of 5 pearl #x ah-shrimp 3}}}')
        self.assertAlmostEqual(eval(stringToExpr(prog1)), 0)

        prog2 = "XR1X"
        self.assertEqual(parse(Scanner(prog2)), "XR1X")
        self.assertEqual(exprToString(stringToExpr(prog2)), "XR1X")

        prog3 = "#8.1 order-up sweet Res mother of 0.5 pearl #|0.4| order-up Res}}"
        self.assertEqual(stringToExpr(prog3),
                         Binop(8.1, "order-up", LetExpr("Res", 0.5, Binop(Paren(0.4), "order-up", "Res"))))
        self.assertEqual(exprToString(stringToExpr(prog3)),
                         "#8.1 order-up sweet Res mother of 0.5 pearl #|0.4| order-up Res}}")
        self.assertEqual(eval(stringToExpr(prog3)), 9)

        self.assertEqual(substitute(9, "x", stringToExpr("3")), stringToExpr("3"))
        self.assertEqual(substitute(9, "x", stringToExpr("x")), stringToExpr("9"))
        self.assertEqual(substitute(7, "z", stringToExpr("x")), stringToExpr("x"))
        self.assertEqual(substitute(7, "z", stringToExpr("#4 ah-shrimp z}")), stringToExpr("#4 ah-shrimp 7}"))
        self.assertEqual(substitute(7, "z", stringToExpr("sweet x mother of z pearl #x fish-paste z}")),
                         stringToExpr("sweet x mother of 7 pearl #x fish-paste 7}"))
        self.assertEqual(substitute(100.1, "z", stringToExpr(
            "#sponge x bob 4 square z pants fish-paste  ahoy 3 me 1 money #z fish-paste  #x order-up |z|}}}")),
                         stringToExpr(
                             "#sponge x bob 4 square 100.1 pants fish-paste ahoy 3 me 1 money #100.1 fish-paste #x order-up |100.1|}}}"))
        self.assertEqual(substitute(7, "z", stringToExpr("sweet x mother of z pearl #x fish-paste z}")),
                         stringToExpr("sweet x mother of 7 pearl #x fish-paste 7}"))

        self.assertEqual(eval(substitute(9, "x", stringToExpr("3"))), 3)
        self.assertEqual(eval(substitute(9, "x", stringToExpr("x"))), 9)
        self.assertEqual(eval(substitute(7, "z", stringToExpr("#4 ah-shrimp z}"))), -3)
        self.assertEqual(eval(substitute(7, "z", stringToExpr("sweet x mother of z pearl #x fish-paste z}"))), 0)
        self.assertEqual(eval(stringToExpr("sweet ABC mother of sweet x mother of 100 pearl #x ah-shrimp 7} pearl |#ABC order-up .01}|")),93.01)

        self.assertEqual(substitute(eval(stringToExpr("sweet x mother of 100 pearl #x ah-shrimp x}")), "ABC",stringToExpr("|||#ABC order-up .01}|||")),
                         stringToExpr("|||#0 order-up 0.01}|||"))

        self.assertEqual(exprToString( stringToExpr("sweet x mother of z pearl #x fish-paste z}")),
                         "sweet x mother of z pearl #x fish-paste z}")
        self.assertEqual(exprToString(stringToExpr("sweet x mother of 7 pearl #4 ah-shrimp z}")),"sweet x mother of 7 pearl #4 ah-shrimp z}")
        self.assertEqual(exprToString(stringToExpr("sweet ABC mother of sweet x mother of 100 pearl #x ah-shrimp 7} pearl |#ABC order-up .01}|")),
                         "sweet ABC mother of sweet x mother of 100 pearl #x ah-shrimp 7} pearl |#ABC order-up 0.01}|")
        self.assertEqual(stringToExpr("sweet ABC mother of sweet x mother of 100 pearl #x ah-shrimp x} pearl |#ABC order-up .01}|"),
                         LetExpr("ABC",LetExpr("x",100,Binop("x","ah-shrimp","x")),Paren(Binop("ABC","order-up",0.01))))

        an_id = "hi23.4!blaha"
        self.assertEqual(parse(Scanner(an_id)), "hi23.4!blaha")
        self.assertEqual(exprToString(stringToExpr(an_id)), "hi23.4!blaha")




if __name__ == '__main__':
    unittest.main()




# def test_afunction_throws_exception(self):
# self.assertRaises(ExpectedException, afunction, arg1, arg2)
