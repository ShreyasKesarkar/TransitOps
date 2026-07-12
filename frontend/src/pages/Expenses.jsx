import ManagementPage from '../components/pages/ManagementPage';
import { managementConfigs } from '../config/entityConfigs';

export default function Expenses() {
  return <ManagementPage config={managementConfigs.expenses} />;
}