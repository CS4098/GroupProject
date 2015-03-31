process test{
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
}
