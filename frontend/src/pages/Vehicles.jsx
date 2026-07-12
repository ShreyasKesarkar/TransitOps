import ManagementPage from '../components/pages/ManagementPage';
import { managementConfigs } from '../config/entityConfigs';

export default function Vehicles() {
  return <ManagementPage config={managementConfigs.vehicles} />;
}