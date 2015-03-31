process test{
	branch br1 {
		selection sel1 {
	        action act1 {
		        requires { a }
		        provides { b }
	        }
	        action act2 {
		        requires { b }
		        provides { e }
	        }
	        action act3 {
		        requires { c }
		        provides { d }
	        }
    	}
   	    selection sel2 {
	        action act4 {
		        requires { a }
		        provides { d }
	        }
	        task t1 {
			    action act5 {
			        requires { a }
			        provides { b }
			    }
			    action act6 {
			        requires { b }
			        provides { c }
			    }
			    action act7 {
			        requires { c }
			        provides { d }
			    }
		    }
	    }
	    selection sel3 {
	        action act8 {
		        requires { a }
		        provides { x }
	        }
	        sequence seq1 {
			    action act9 {
			        requires { a }
	                provides { c }
			    }
	            action act10 {
			        requires { c }
	                provides { x }
			    }
		    }
	    }
	}
}
