import express from 'express';
import dotenv from 'dotenv';
import authRouter from './routes/authRouter';
import equipmentRouter from './routes/equipmentRouter';
import loanRouter from './routes/loanRouter';
import { startScheduler } from './scheduler';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ヘルスチェック
app.get('/health', (_req, res) => {
  res.json({ status: 'ok' });
});

app.use('/auth', authRouter);
app.use('/equipments', equipmentRouter);
app.use('/loans', loanRouter);

if (process.env.NODE_ENV !== 'test') {
  app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
    startScheduler();
  });
}

export default app;
