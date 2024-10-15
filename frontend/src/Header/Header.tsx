import "./Header.scss";
import { Link } from "react-router-dom";
import Logo from "../assets/icons/Logo.svg";
import LigthThemeSwift from "../assets/icons/DayNightSwitch.svg";
import Avatar from "../assets/images/avatar.png";

function Header() {
  return (
    <header className="header">
      <div className="header__logo-group">
        <Link to="/" className="header__logo">
          <img src={Logo} alt="РосБанк" />
        </Link>
        <h1 className="header__title">SuperStars</h1>
      </div>
      <div className="header__user">
        <img
          className="header__swift"
          src={LigthThemeSwift}
          alt="Здесь будет переключение темы"
        />
        <img className="header__photo" src={Avatar} alt="фото пользователя" />
      </div>
    </header>
  );
}

export default Header;
