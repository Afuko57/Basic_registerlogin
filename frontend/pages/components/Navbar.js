import Link from "next/link";
import "bootstrap/dist/css/bootstrap.min.css";

import { useState } from "react";
import { useRouter } from "next/router";

const Navbar = ({ setUserName, username }) => {
  const router = useRouter();

  const [loggedIn, setLoggedIn] = useState(!!username);

  const handleLogin = () => {
    router.push({
      pathname: "/",
      query: { username },
    });
  };

  const handleLogout = () => {
    setLoggedIn(false);
    setUserName("");
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <div className="collapse navbar-collapse">
        <ul className="navbar-nav mr-auto">
          <li className="nav-item">
            <Link href="/" className="nav-link">
              Home
            </Link>
          </li>
          <li className="nav-item">
            <Link href="/about" className="nav-link">
              About
            </Link>
          </li>
          <li className="nav-item">
            <Link href="/login" className="nav-link">
              Log in
            </Link>
          </li>
          <li className="nav-item">
            {/* เมื่อล็อคอินต้องการให้ชื่อ user ปรากฏตรงนี้ */}
          </li>
        </ul>

        <ul className="navbar-nav mr-auto">
          {loggedIn && (
            <li className="nav-item">
              <span className="nav-link">Welcome, {username}</span>
            </li>
          )}
        </ul>

        <div className="d-flex">
       <button onClick={handleLogout}>Logout</button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
