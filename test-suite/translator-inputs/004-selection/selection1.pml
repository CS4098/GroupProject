process test {
    selection {
        action act1 {
	        requires { a }
	        provides { a }
        }
        sequence one {
		    action act2 {
		        requires { a }
                provides { c }
		    }
            action act3 {
		        requires { c }
                provides { b }
		    }
	    }
    }
}

