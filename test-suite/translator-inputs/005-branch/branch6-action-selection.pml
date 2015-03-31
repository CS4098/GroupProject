process test{
	branch br1 {
		action act1 {
		requires { a }
		provides { e }
		}
		selection sel1 {
	        action act2 {
		        requires { a }
		        provides { b }
	        }
	        action act3 {
		        requires { b }
		        provides { e }
	        }
	        action act4 {
		        requires { c }
		        provides { d }
	        }
    	}
	}
}
