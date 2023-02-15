import React from "react";

function Footer() {
  return (
    <footer
      style={{
        backgroundColor: "#FB8500",
        color: "white",
        textAlign: "center",
        position: "fixed",
        bottom: "0px",
        left: "0px",
        right: "0px"
      }}
    >
      Copyright &copy; {new Date().getFullYear()} Your Company
    </footer>
  );
}

export default Footer;
