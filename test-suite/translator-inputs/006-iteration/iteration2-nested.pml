process iteNest {

    iteration {
        action a {
            provides { c }
        }
        iteration {
            action c {
                requires { c }
                provides { d }
            }
            action d {
                requires { d }
                provides { b }
            }
        }
        action b {
            requires { b }
        }
    }
}
