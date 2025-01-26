import React, { useEffect, useState } from 'react';
import { Navbar, Nav, Button } from 'react-bootstrap';
import { LinkLink } from 'react-router-dom';
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
            {/* <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">
                    <Nav.Link as={Link} to="/" className="d-flex align-items-center">
                        <FaHome style={{ marginRight: '8px' }} /> Home
                    </Nav.Link>
                    <Nav.Link as={Link} to="/inventory" className="d-flex align-items-center">
                        <FaBoxOpen style={{ marginRight: '8px' }} /> Inventory
                    </Nav.Link>
                    <Nav.Link as={Link} to="/recipes" className="d-flex align-items-center">
                        <FaBook style={{ marginRight: '8px' }} /> Recipes
                    </Nav.Link>
                    <Nav.Link as={Link} to="/add-item" className="d-flex align-items-center">
                        <FaPlusCircle style={{ marginRight: '8px' }} /> Add Groceries
                    </Nav.Link>
                </Nav>
                <div className="d-flex align-items-center ml-auto mt-3 mt-lg-0" style={{ justifyContent: 'flex-end', flexGrow: 1 }}>
                    {isLoggedIn && username ? (
                        <>
                            <FaUserCircle style={{ color: 'white', marginRight: '10px', fontSize: '1.5rem' }} />
                            <span style={{ color: 'white', marginRight: '15px', fontWeight: 'bold' }}>{username}</span>
                            <Button variant="outline-light" onClick={handleLogout} className="d-flex align-items-center">
                                <FaSignOutAlt style={{ marginRight: '5px' }} /> Logout
                            </Button>
                        </>
                    ) : (
                        <Button as={Link} to="/login" variant="outline-light" className="d-flex align-items-center" onClick={() => navigate('/login')}>
                            <FaSignInAlt style={{ marginRight: '5px' }} /> Login
                        </Button>
                    )}
                </div>
            </Navbar.Collapse> */}
        </Navbar>
    );
}

export default Header;
