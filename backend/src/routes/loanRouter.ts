import { Router } from 'express';
import { authenticate, requireRole } from '../middleware/auth';
import * as loanController from '../controllers/loanController';

const router = Router();

router.post('/', authenticate, requireRole('ADMIN'), loanController.createLoan);
router.post('/:id/return', authenticate, requireRole('ADMIN'), loanController.returnLoan);
router.get('/user/:userId', authenticate, requireRole('USER', 'ADMIN'), loanController.getLoansByUser);
router.get('/equipment/:equipmentId', authenticate, requireRole('ADMIN'), loanController.getLoansByEquipment);

export default router;
