import { Router } from 'express';
import { login } from '../controllers/authController';

const authRouter = Router();

authRouter.post('/login', login);

export default authRouter;
