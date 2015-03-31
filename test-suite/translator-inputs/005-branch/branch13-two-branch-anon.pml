process test{
	sequence seq1 {
		branch {
			action act_1 {
			requires { a }
			provides { b }
			}
			action act_2 {
			requires { b }
			provides { c }
			}
			action act_3 {
			requires { a }
			provides { c }
			}
		}
		branch {
			action act_4 {
			requires { d }
			provides { e }
			}
			action act_5 {
			requires { e }
			provides { f }
			}
		}
	}
}
