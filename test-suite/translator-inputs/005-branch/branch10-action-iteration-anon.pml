process test{
	branch br1 {
		action act1 {
		requires { a }
		provides { e }
		}
		iteration {
            action act2 {
                requires { c }
                provides { d }
            }
            action act3 {
                requires { d }
                provides { b }
            }
        }
	}
}
