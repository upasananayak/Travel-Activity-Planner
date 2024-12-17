import { Outlet, Navigate } from 'react-router-dom';

const ProtectedRoute = () => {
    const token = localStorage.getItem('Token');
    console.log(token)
    return token ? <Outlet /> : <Navigate to="/login" replace />;
};

export default ProtectedRoute;
