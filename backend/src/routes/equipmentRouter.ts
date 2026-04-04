import { Router } from 'express';
import { authenticate, requireRole } from '../middleware/auth';
import * as equipmentController from '../controllers/equipmentController';
import * as searchController from '../controllers/searchController';

const router = Router();

router.post('/', authenticate, requireRole('ADMIN'), equipmentController.createEquipment);
router.get('/', authenticate, requireRole('USER', 'ADMIN'), equipmentController.getEquipments);
router.get('/search', authenticate, requireRole('USER', 'ADMIN'), searchController.searchEquipments);
router.get('/:id', authenticate, requireRole('USER', 'ADMIN'), equipmentController.getEquipmentById);
router.put('/:id', authenticate, requireRole('ADMIN'), equipmentController.updateEquipment);
router.delete('/:id', authenticate, requireRole('ADMIN'), equipmentController.disposeEquipment);

export default router;
