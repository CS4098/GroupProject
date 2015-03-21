process test{
	branch br1 {
		action act_1 {
		requires { a }
		provides { e }
		}
		sequence seq_1 {
			action act_2 {
			requires { b }
			provides { c }
			}
			action act_3 {
			requires { c }
			provides { d }
			}
			action act_4 {
			requires { d }
			provides { e }
			}
		}
	}
}
