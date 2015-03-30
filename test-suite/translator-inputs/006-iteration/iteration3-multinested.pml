process iteNest {

    action a {}
    iteration {
        action b {}
        iteration  {
            action c {}
            iteration {
                action d {}
            }
        }
    }
    action d {}
}
