process test {
    selection {
        action act1 {
	        requires { a }
	        provides { a }
        }
        task one {
		    action a {
		        requires { a }
		        provides { b }
		    }
		    action b {
		        requires { b }
		        provides { c }
		    }
		    action c {
		        requires { c }
		        provides { d }
		    }
	    }
    }
}

