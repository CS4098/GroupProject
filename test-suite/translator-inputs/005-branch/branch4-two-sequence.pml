process test{
	branch br1 {
		sequence seq1 {
			action act_1 {
			requires { a }
			provides { b }
			}
			action act_2 {
			requires { b }
			provides { c }
			}
		}
		sequence seq2 {
			action act_3 {
			requires { d }
			provides { e }
			}
			action act_4 {
			requires { e }
			provides { f }
			}
		}
	}
}
