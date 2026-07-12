import ManagementPage from '../components/pages/ManagementPage';
import { managementConfigs } from '../config/entityConfigs';

export default function Maintenance() {
  return <ManagementPage config={managementConfigs.maintenance} />;
}