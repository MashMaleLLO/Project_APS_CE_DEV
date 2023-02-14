import React from 'react';

function Footer() {
  return (
    <footer style={{ backgroundColor: '#FB8500', color: 'white' ,textAlign: 'center'}}>
      Copyright &copy; {new Date().getFullYear()} Your Company
    </footer>
  );
}

export default Footer;