import React, { useEffect, useState } from 'react';
import { Navbar, Nav, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { FaSignInAlt, FaUserCircle, FaSignOutAlt, FaHome, FaBoxOpen, FaBook, FaPlusCircle } from 'react-icons/fa';

function Header() {
    return (
        <Navbar bg="dark" variant="dark" expand="lg" className="px-3">
            <Navbar.Brand href="/" className="d-flex align-items-center">
                <img
                    src={`${process.env.PUBLIC_URL}/logo.png`}
                    alt="MarketPulse Logo"
                    width="30"
                    height="30"
                    className="d-inline-block align-top"
                    style={{ marginRight: '10px' }}
                />
                MarketPulse
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">
                    <Nav.Link as={Link} to="/" className="d-flex align-items-center">
                        <FaHome style={{ marginRight: '8px' }} /> Dashboard
                    </Nav.Link>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    );
}

export default Header;
