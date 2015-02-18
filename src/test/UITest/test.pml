process implement_peos {
    action checkout {
        requires { repository }
    provides { workspace }
    }
    action check_tcltk {
    }
    action goto_kernel_dir {
        requires { workspace }
    }
}