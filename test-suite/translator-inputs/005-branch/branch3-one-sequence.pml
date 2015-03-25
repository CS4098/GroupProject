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
	}
}
