import ManagementPage from '../components/pages/ManagementPage';
import { managementConfigs } from '../config/entityConfigs';

export default function Users() {
  return <ManagementPage config={managementConfigs.users} />;
}